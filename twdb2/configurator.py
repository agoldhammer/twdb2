#! /usr/bin/env python

"""
Configuration module for twdb app
"""

import configparser
import os
import sys

config = configparser.ConfigParser()

twdbConfig = {}

# TODO: change to read from user's home dir'
# TODO: think about better placement/invocation for the config file
# config.read('twdb.conf')
# config.read(os.path.expanduser('~/.twdb2.conf'))

# must set environment variable TWDBCONF to path of config file
config_file = os.getenv("TWDBCONF")
if config_file:
    config.read(os.path.expanduser(config_file))
else:
    print("Config error: env var TWDBCONF not set")
    sys.exit(255)

twdbConfig['OAUTH_TOKEN'] = config.get('authentication', 'OAUTH_TOKEN')
twdbConfig['OAUTH_TOKEN_SECRET'] = config.get('authentication',
                                              'OAUTH_TOKEN_SECRET')
twdbConfig['CONSUMER_KEY'] = config.get('authentication', 'CONSUMER_KEY')
twdbConfig['CONSUMER_SECRET'] = config.get('authentication', 'CONSUMER_SECRET')

host = config.get('db', "HOST")
twdbConfig['DBHOST'] = 'localhost' if host is None else host
twdbConfig['DBNAME'] = config.get('db', 'DBNAME')

twdbConfig['authfile'] = config.get('authors', 'authfile')
twdbConfig['topicsfile'] = config.get('topics', 'topicsfile')
twdbConfig['logfile'] = config.get('logging', 'logfile')
twdbConfig['logname'] = config.get('logging', 'logname')
twdbConfig['owner'] = config.get('twitter', 'owner')
twdbConfig['slug'] = config.get('twitter', 'slug')

if __name__ == '__main__':
    print(twdbConfig)
