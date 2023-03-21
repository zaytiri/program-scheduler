import yaml


def write_yaml(path, configs):
    config_file = open(path, 'w')
    yaml.safe_dump(configs, config_file)
    config_file.close()


def read_yaml(path):
    config_file = open(path, 'r')
    configs = yaml.safe_load(config_file)
    config_file.close()
    return configs
