import json
from collections import namedtuple
import pkg_resources
import os

Config = namedtuple('Config',
                    ('env_host_name','api_host_name', 'data_server', 'auth_path', 'auth_uri',
                     'login_details','boxset_auth_path','boxset_auth_uri',
                     'oracle_db_connection_string'))

__INSTANCE = None  # lazy-assigned instance


def instance():
    global __INSTANCE

    if __INSTANCE is not None:
        return __INSTANCE
    else:
        config_file = pkg_resources.resource_filename(__name__, "config.json")
        with open(config_file) as config_file:
            config_data = json.load(config_file)

        environment = os.environ.get('VOD_ENVIRONMENT', "default")
        env = config_data['environment']

        servers = env.get(environment, env['default'])

        user_name = config_data['user']['username']
        password = config_data['user']['password']
        auth_path = config_data['auth_path']
        boxset_auth_path = config_data['boxset_auth_path']

        print "-----------------------------"
        print "Running with %s configuration" % environment
        print "Api server: %s" % servers['api_server']
        print "Auth server: %s" % servers['auth_server']
        print "Database: %s" % servers['db_server']
        print "User: %s" % user_name
        print "-----------------------------"

        __INSTANCE = Config(
            env_host_name=servers['auth_server'],
            api_host_name=servers['api_server'],
            data_server=servers['data_server'],
            auth_path=auth_path,
            boxset_auth_path=boxset_auth_path,
            auth_uri="http://%s:831/%s" % (servers['auth_server'], auth_path),
            boxset_auth_uri="http://%s:820/%s" % (servers['auth_server'], boxset_auth_path),
            login_details=(user_name, password),
            oracle_db_connection_string="%s/%s@%s" % (user_name, password, servers['db_server'])
        )

        return __INSTANCE
