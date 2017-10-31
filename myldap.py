#!/usr/bin/env python
# encoding: utf-8

"""
CLI to interact with an OpenLDAP instance.
Requires: python3, pyldap, click
"""

import ldap
import os
import random
import string


LDAP_SERVER = os.environ.get('LDAP_SERVER')
LDAP_TOP_DN = os.environ.get('LDAP_TOP_DN')
LDAP_ADMIN_DN = os.environ.get('LDAP_ADMIN_DN')
LDAP_ADMIN_PASSWORD = os.environ.get('LDAP_ADMIN_PASSWORD')

LDAP_CONN = ldap.initialize(LDAP_SERVER)
LDAP_CONN.bind(LDAP_ADMIN_DN, LDAP_ADMIN_PASSWORD)


class User(object):
    """LDAP User"""

    def __init__(self, username):
        self.username = username
        # we lookup in LDAP if user really exists under this username
        result = LDAP_CONN.search_s(
            LDAP_TOP_DN,
            ldap.SCOPE_ONELEVEL,
            filterstr='(uid={})'.format(self.username)
            )
        if len(result) == 1:
            for dn, infos in result:
                self.dn = dn
                for key, values in infos.items():
                    if key not in ['userPassword', 'uid']:
                        value = values[0].decode('utf-8')
                        setattr(self, key, value)
        elif not result:
            raise ValueError('{} does not exist'.format(self.username))
        else:
            raise ValueError('{} is not unique'.format(self.username))

    def __repr__(self):
        return '<User {}>'.format(self.dn)

    def update(self, key, value):
        """Modify attribute for user.
        Attribute must be a recognize type in LDAP (e.g givenName, sn, etc.)"""
        value = value.encode('utf-8')
        LDAP_CONN.modify_s(self.dn, [(ldap.MOD_REPLACE, key, value)])

    def delete(self):
        LDAP_CONN.delete_s(self.dn)

    def passwd(self, old_password, new_password):
        LDAP_CONN.passwd_s(self.dn, old_password, new_password)
