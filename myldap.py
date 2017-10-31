#!/usr/bin/env python
# encoding: utf-8

"""
CLI to interact with an OpenLDAP instance.
Requires: python3, pyldap, click
"""


import click
import getpass
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

    @staticmethod
    def generate_random_password():
        choices = string.ascii_letters + string.digits
        new_password = ''.join(random.sample(choices, random.randint(8, 16)))
        return new_password

    @staticmethod
    def search(key=None, value=None):
        """Search LDAP according to key parameters"""
        if key and value:
            result = LDAP_CONN.search_s(
                LDAP_TOP_DN,
                ldap.SCOPE_ONELEVEL,
                filterstr='({0}={1})'.format(key, value)
                )
        elif not key and not value:
            result = LDAP_CONN.search_s(
                LDAP_TOP_DN,
                ldap.SCOPE_ONELEVEL
                )
        else:
            result = []
        return result


    @staticmethod
    def create(common_name, first_name, last_name, username):
        """Create an account"""
        if User.search('cn', common_name):
            raise ValueError('{} already exists'.format(common_name))
        elif User.search('uid', username):
            raise ValueError('{} already exists'.format(username))
        else:
            data = {
                'uid': username,
                'givenName': first_name,
                'sn': last_name,
                'cn': common_name,
                'objectClass': 'inetOrgPerson'
                }
            data = [
                (key, value.encode('utf-8')) for key, value in data.items()
                ]
            LDAP_CONN.add_s(LDAP_TOP_DN, data)
            user = User(username)
            user.reset()

    def update(self, key, value):
        """Modify attribute for user.
        Attribute must be a recognize type in LDAP (e.g givenName, sn, etc.)"""
        value = value.encode('utf-8')
        LDAP_CONN.modify_s(self.dn, [(ldap.MOD_REPLACE, key, value)])

    def delete(self):
        LDAP_CONN.delete_s(self.dn)

    def passwd(self, old_password, new_password):
        """Modify password"""
        LDAP_CONN.passwd_s(self.dn, old_password, new_password)

    def reset(self):
        """Reset user's password"""
        self.update('userPassword', self.username)
        new_password = User.generate_random_password()
        self.passwd(self.username, new_password)
        print('New password is {}. Please change it'.format(new_password))


@click.group()
def cli():
    pass


@cli.command()
@click.argument('attr')
def search(attr):
    """Search LDAP"""
    key, value = attr.split('=')
    if key not in ['cn', 'uid', 'sn', 'givenName']:
        msg = ("attr represents data like key=value "
               "where key is in ['cn', 'uid', 'sn', 'givenName'] "
               "and value is an expression")
        click.echo(msg)
    else:
        result = search(key, value)
        for dn, infos in result:
            user = User(infos['uid'][0].decode('utf-8'))
            for key, value in user.__dict__.items():
                if key != 'userPassword':
                    click.echo('{0}: {1}'.format(key, value))
            click.echo('\n')


@cli.command()
@click.argument('username')
def get(username):
    """Display infos about user"""

    try:
        user = User(username)
    except ValueError as exc:
        click.echo(exc)
    else:
        for key, value in user.__dict__.items():
            if key != 'userPassword':
                click.echo('{0}: {1}'.format(key, value))


@cli.command()
@click.argument('common_name')
@click.argument('first_name')
@click.argument('last_name')
@click.argument('username')
def create(common_name, first_name, last_name, username):
    """Create account for a new user"""

    User.create(common_name, first_name, last_name, username)


@cli.command()
@click.argument('username')
def reset(username):
    """Reset username's password"""

    try:
        user = User(username)
    except ValueError as exc:
        click.echo(exc)
    else:
        user.reset()


@cli.command()
@click.argument('username')
def passwd(username):
    """Modify user's password"""

    try:
        user = User(username)
    except ValueError as exc:
        click.echo(exc)
    else:
        old_password = getpass.getpass(prompt='Old password')
        new_password = getpass.getpass(prompt='New password')
        new_password_confirm = getpass.getpass(prompt='Confirm new password')
        if new_password == new_password_confirm:
            user.passwd(old_password, new_password)
        else:
            msg = 'Please make sure to enter the same value for new password'
            click.echo(msg)


@cli.command()
@click.argument('username')
@click.option('--attr', help='update attribute with attrname=value')
def update(username, attr):
    """Update user's attribute"""

    try:
        user = User(username)
    except ValueError as exc:
        click.echo(exc)
    else:
        attr, value = attr.split('=')
        user.update(attr, value)


@cli.command()
@click.argument('username')
def delete(username):
    """Delete user from ldap"""

    try:
        user = User(username)
    except ValueError as exc:
        click.echo(exc)
    else:
        user.delete()
        click.echo('{} has been deleted'.format(username))


if __name__ == '__main__':
    cli()

# EOF
