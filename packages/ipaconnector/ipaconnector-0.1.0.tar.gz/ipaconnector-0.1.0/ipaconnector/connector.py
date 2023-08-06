import getpass
import socket
import json
import logging

from python_freeipa import ClientMeta
from python_freeipa.exceptions import Unauthorized

from ipaconnector.constans import ELARA, GANYMEDE, CALLISTO, LEDA
from ipaconnector.jdbc import PrivateZone
from ipaconnector.kerberos import Kerberos
from ipaconnector.klass import User, Group, AppUser
from ipaconnector.sshwrapper import SSHConn, Shell


class IpaConnector:
    def __init__(self, host):
        self._log = logging.getLogger('ipa-connector')
        self._log.info(f"IPA SERVER: {host}")
        self.client = ClientMeta(host=host, verify_ssl=False, dns_discovery=False)
        self.cluster = self._get_cluster(socket.gethostname())
        self._passwd = None
        self._keytab_creations = []
        self.keytab_host = self.cluster.HOST

    def run(self, path: str):
        """
        Runs everything.
        """
        self.to_add, self.to_update, self.to_delete = self.read_input(path)
        self.make_add()
        self.make_update()
        self.make_delete()
        if self._keytab_creations:
            self.create_keytabs(self.keytab_host)

    def make_add(self):
        users = self._add_users()
        self._add_groups()
        for user in users:
            user.apply_roles(self.client)
        self._add_hive_dbs()

    def make_update(self):
        self._update_groups()
        self._update_users()
        self._update_hive_dbs()

    def _update_groups(self):
        all_groups = self.to_update.get('UserGroup', []) + self.to_update.get('AppUserGroup', [])
        [Group(group_data).update_members(self.client) for group_data in all_groups]

    def _update_users(self):
        app_users = [AppUser(user_data) for user_data in self.to_update.get('AppUser', [])]
        human_users = [User(user_data) for user_data in self.to_update.get('HumanUser', [])]
        all_users = human_users + app_users
        self._keytab_creations.extend([user for user in human_users if user.keytab is True])
        for user in all_users:
            user.apply_roles(self.client)

    def make_delete(self):
        self._delete_users()
        self._delete_groups()
        self._delete_hive_dbs()

    def _delete_users(self):
        human_users = [User(user_data) for user_data in self.to_delete.get('HumanUser', [])]
        app_users = [AppUser(user_data) for user_data in self.to_delete.get('AppUser', [])]
        for user in human_users + app_users:
            user.delete(self.client)

    def _delete_groups(self):
        all_groups = self.to_delete.get('UserGroup', []) + self.to_delete.get('AppUserGroup', [])
        for group_data in all_groups:
            Group(group_data).delete(self.client)

    def _delete_hive_dbs(self):
        # TODO
        self._log.info("Delete hive dbs is not implemented yet.")
        pass

    def _add_groups(self):
        all_groups = self.to_add.get('AppUserGroup', []) + self.to_add.get('UserGroup', [])
        for group_data in all_groups:
            Group(group_data).add(self.client)

    def _add_users(self):
        human_users = [User(user_data) for user_data in self.to_add.get('HumanUser', '')]
        app_users = [AppUser(user_data) for user_data in self.to_add.get('AppUser', '')]
        all_users = human_users + app_users
        for user in all_users:
            user.add(self.client)
        self._keytab_creations.extend([user for user in human_users if user.keytab is True])
        return all_users

    def _add_hive_dbs(self):
        all_hive_dbs = [PrivateZone(group_data) for group_data in self._get_hive_dbs(self.to_add)]
        for db in all_hive_dbs:
            cluster = self._get_cluster(db.cluster)
            if cluster == self.cluster:
                db.add_new_database(cluster.get_hive_interface())
            else:
                self._log.info("not this cluster")

    def connect(self, user=None, password=None, kerberos=False):
        if kerberos:
            self._log.info("Authenticating via kerberos")
            self._connect_kerberos()
            return
        if not user and not password:
            raise RuntimeError("Credentials not provided")
        self._log.info("Authenticating via credentials")
        self._passwd = password
        self.client.login(user, password)

    def _connect_kerberos(self):
        """
        Make connection to IPA server
        """
        self._log.info("Connecting to IPA")
        try:
            self.client.login_kerberos()
        except Unauthorized:
            self._log.debug("Unauthorized, acquiring TGT...")
            Kerberos().acquire_tgt()
            self._log.debug("Retrying login")
            self.client.login_kerberos()

    def _get_cluster(self, host):
        if "ganymede" in host:
            cluster = GANYMEDE
        elif "callisto" in host:
            cluster = CALLISTO
        elif "leda" in host:
            cluster = LEDA
        else:
            cluster = ELARA
        return cluster

    def _open_as_json(self, path: str) -> dict:
        """
        path: full or relative path to input file
        Usually given via command line - see scripts/
        """
        with open(path, 'r') as _file:
            content = json.load(_file)
        return content

    def _generate_keytab_create_cmd(self, user):
        cmds = [
            f"ipa service-add {user.login}/$(hostname -f)",
            f"ipa-getkeytab -p {user.login}/$(hostname -f) -k {user.login}.keytab",
            f"sudo chown {user.login}. {user.login}.keytab",
            f"sudo mkhomedir_helper {user.login} 0027",
            f"sudo mv {user.login}.keytab /data01/{user.login}/",
        ]
        return cmds

    def create_keytabs(self, server="elara-edgeg-u1-n01"):
        user = None
        if not user:
            user = getpass.getuser()
        s_hostname = socket.gethostname()
        if s_hostname in server or server in s_hostname:
            shell = Shell(user=user)
        else:
            shell = SSHConn(server, user, self._passwd)

        with shell:
            shell.kinit(cluster=self.cluster)
            for user in self._keytab_creations:
                cmds = self._generate_keytab_create_cmd(user)
                shell.execute(cmd_list=cmds)

    def read_input(self, path: str) -> tuple:
        """
        path: path to input json file
        return: list of actions required
        """
        self._log.info(f"Reading file {path}")
        input_data = self._open_as_json(path)
        self._log.debug(f"{input_data}")
        to_add = input_data['CREATIONS']
        to_delete = input_data['DELETIONS']
        to_update = input_data['UPDATES']
        return to_add, to_update, to_delete

    def _get_hive_dbs(self, _dict):
        hive_db = list()
        for i in ["ExploitedZone", "PrivateZone", "DevZone"]:
            zone = _dict.get(i, None)
            if zone:
                hive_db.extend(_dict[i])
        return hive_db

    def _update_hive_dbs(self):
        all_hive_dbs = [PrivateZone(group_data) for group_data in self._get_hive_dbs(self.to_update)]
        for db in all_hive_dbs:
            cluster = self._get_cluster(db.cluster)
            if cluster != self.cluster:
                self._log.info("not this cluster")
            db.update_group_grant_on_role(cluster.get_hive_interface())
