import json

from django.apps import AppConfig

from radeclaRest.settings import BASE_DIR


class ConfigConfig(AppConfig):
    name = 'config'


def read_config():
    with open(BASE_DIR + '/' + ConfigConfig.name + '/config.json', 'r') as f:
        config = json.loads(f.read())
    return config


def write_config(**kwargs):
    config = read_config()
    for key, val in kwargs.items():
        config[key] = val
    with open(BASE_DIR + '/' + ConfigConfig.name + '/config.json', 'w') as f:
        f.write(json.dumps(config, indent=2))

    return config
