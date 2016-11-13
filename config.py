import argparse
import os
import random
import string

description = 'Create a credentials configuration file. The credentials will' \
              ' be stored in plain text.'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('--dbengine', action='store', nargs='?',
                    default='django.db.backends.sqlite3',
                    help='The database backend to use. Supports non-built-in '
                         'database backends.')
parser.add_argument('--dbname', action='store', nargs='?',
                    default=os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'openbudget.sqlite3'),
                    help='The name of the database to use. For SQLite, it’s '
                         'the full path to the database file. When specifying '
                         'the path, always use forward slashes, even on '
                         'Windows (e.g. C:/homes/user/mysite/sqlite3.db).')
parser.add_argument('--dbuser', action='store', nargs='?',
                    default='',
                    help='The username to use when connecting to the database.'
                         ' Not used with SQLite.')
parser.add_argument('--dbpassword', action='store', nargs='?',
                    default='',
                    help='The password to use when connecting to the database.'
                         ' Not used with SQLite.')
parser.add_argument('--dbhost', action='store', nargs='?',
                    default='',
                    help='Which host to use when connecting to the database. '
                         'An empty string means localhost. Not used with '
                         'SQLite.')
parser.add_argument('--dbport', action='store', nargs='?',
                    default='',
                    help='The port to use when connecting to the database. An '
                         'empty string means the default port. Not used with '
                         'SQLite.')
parser.add_argument('--debug', action='store_const', const=True, default=False,
                    help='Turn on debug mode.')
parser.add_argument('--hosts', action='store', nargs='*',
                    default=['localhost', '127.0.0.1', '[::1]'],
                    help='The host/domain names that this Django site can '
                         'serve. First host will be used as the current site.')
args = vars(parser.parse_args())

# Create credentials file

credentials_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'openbudget', 'credentials.py')
fixture_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'fixture_sites.yaml')
chars = ''.join([string.ascii_letters, string.digits, string.punctuation]) \
    .replace('\'', '') \
    .replace('"', '') \
    .replace('\\', '')
secret_key = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

with open(credentials_filepath, 'w') as file:
    file.writelines([
        'DATABASE_ENGINE = \'{}\'\n'.format(args['dbengine']),
        'DATABASE_NAME = \'{}\'\n'.format(args['dbname']),
        'DATABASE_USER = \'{}\'\n'.format(args['dbuser']),
        'DATABASE_PASSWORD = \'{}\'\n'.format(args['dbpassword']),
        'DATABASE_HOST = \'{}\'\n'.format(args['dbhost']),
        'DATABASE_PORT = \'{}\'\n'.format(args['dbport']),
        'SECRET_KEY = \'{}\'\n'.format(secret_key),
        'DEBUG = \'{}\'\n'.format(args['debug']),
        'ALLOWED_HOSTS = {}\n'.format(args['hosts']),
        'SITE_ID = 1\n'
    ])

with open(fixture_filepath, 'w') as file:
    file.writelines([
        '- model: sites.site\n',
        '  pk: 1\n',
        '  fields:\n',
        '    domain: {}\n'.format(args['hosts'][0]),
        '    name: {}\n'.format(args['hosts'][0]),
    ])
