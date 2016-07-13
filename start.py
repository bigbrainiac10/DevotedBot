import configparser
import os.path
import sys

from quarry.net.client import ClientProtocol, ClientFactory
from quarry.mojang.profile import Profile

CONFIG_FILE = 'config.cfg'


class DevotedBotClientProtocol(ClientProtocol):
    pass


class DevotedBotClientFactory(ClientFactory):
    protocol = DevotedBotClientProtocol


def generate_config_file(name, config):
    config['auth'] = {'username': 'USERNAME',
                      'password': 'PASSWORD',
                      'auth': 'true'}
    config['server'] = {'ip': 'play.devotedmc.com',
                        'port': '25565'}
    with open(name, 'w') as configfile:
        configfile.write('# Config automatically generated. Delete this file to reset.\n\n')
        config.write(configfile)
    print('Config file generated. Edit the username and password fields to set up an account.')
    sys.exit()


def main():
    cfg = configparser.ConfigParser()
    if os.path.isfile(CONFIG_FILE):
       cfg.read(CONFIG_FILE)
    else:
        generate_config_file(CONFIG_FILE, cfg)

    profile = Profile()
    factory = DevotedBotClientFactory()
    if not cfg['auth'].getboolean('auth'):
        profile.login_offline(cfg['auth']['username'])
        factory.profile = profile
    else:
        def login_ok(data):
            factory.connect(cfg['server']['ip'], int(cfg['server']['port']))

        def login_failed(err):
            print('login failed:', err.value)
            factory.stop()
            sys.exit(1)

        factory.profile = profile
        deferred = profile.login(cfg['auth']['username'], cfg['auth']['password'])
        deferred.addCallbacks(login_ok, login_failed)
        factory.run()


if __name__ == '__main__':
    main()