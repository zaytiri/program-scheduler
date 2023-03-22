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

    @staticmethod
    def get_configs(file_path):
        list_of_configs = read_yaml(file_path)

        current_configurations_list = 'Scheduled jobs:'

        for alias, values in list_of_configs.items():
            current_configurations_list += '\n\t\t\t' + str(alias) + ':\n\t\t\t\t'
            for name, value in values.items():
                current_configurations_list += str(name) + ': ' + str(value) + '\n\t\t\t\t'

        show(current_configurations_list)

    @staticmethod
    def get_global_configs(file_path):
        list_of_configs = read_yaml(file_path)

        current_configurations_list = 'Global settings:\n\t\t\t\t'
        for name, value in list_of_configs.items():
            current_configurations_list += str(name) + ': ' + str(value) + '\n\t\t\t\t'

        show(current_configurations_list)
