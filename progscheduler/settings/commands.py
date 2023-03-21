import sys

from progscheduler.utils.log import show, throw
from progscheduler.utils.yaml import read_yaml, write_yaml


class Commands:

    @staticmethod
    def delete_config(user_arguments, file_path):
        saved_configs = read_yaml(file_path)

        try:
            saved_configs.pop(user_arguments.delete)
        except KeyError:
            throw('\"' + user_arguments.delete + '\" setting does not exist.')

        if saved_configs:
            write_yaml(file_path, saved_configs)
        else:
            file_path.open('w').close()

        show('The following configuration \n\t\t\t\'' + user_arguments.delete + '\'\n\t\t was deleted.')

        sys.exit()

    @staticmethod
    def get_configs(file_path):
        list_of_configs = read_yaml(file_path)

        current_configurations_list = 'Current configurations:'
        for key in list_of_configs:
            current_configurations_list += \
                '\n\t\t\t' + str(list_of_configs[key]['alias']) + ':\n\t\t\t\t' \
                + 'alias: ' + str(list_of_configs[key]['alias']) + '\n\t\t\t\t' \
                + 'path: ' + str(list_of_configs[key]['path']) + '\n\t\t\t\t' \
                + 'days: ' + str(list_of_configs[key]['days']) + '\n\t\t\t\t' \
                + 'time: ' + str(list_of_configs[key]['time']) + '\n\t\t\t\t'

        show(current_configurations_list)

        sys.exit()
