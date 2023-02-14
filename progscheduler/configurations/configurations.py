import os
import sys

import yaml

from progscheduler.entities.prog_arguments import ProgArguments
from progscheduler.services.directory import Directory
from progscheduler.services.file import File
from progscheduler.utils.information import show


class Configurations:
    original_arguments = None
    arguments = ProgArguments()
    settings = {}
    path = os.path.dirname(os.path.realpath(__file__)) + '\\userconfigs.yaml'
    file = File(path)

    def set_original_arguments(self, original_arguments):
        self.original_arguments = original_arguments

    def process(self, to_configure):
        self.arguments.configure = to_configure
        self.__check_deletion_of_config()
        self.__check_list_all_configs()

        if self.is_configured():
            try:
                self.settings = self.__read_yaml()[self.original_arguments.file_alias]
            except (AttributeError, KeyError):
                pass

        if self.arguments.configure:
            self.__configure()

        return self.__get_configs_from_file()

    def is_configured(self):
        directory = Directory(self.file.path)
        if not directory.exists():
            return False

        if self.file.is_empty():
            return False
        return True

    def __configure(self):
        """
        creates a new file and writes all mandatory arguments
        """
        arguments = self.arguments.to_list()

        for configuration in arguments:
            self.settings[configuration.name] = self.__process_configuration(configuration)

        self.__write_to_file()

        self.arguments.from_list(arguments)

        show('The following configuration \n\t\t\t\'' + str(self.arguments.file_alias.value) + '\'\n\t\t was added/updated:\n\t\t\t'
             + str(self.arguments.file_alias.name) + ': ' + str(self.arguments.file_alias.value) + '\n\t\t\t'
             + str(self.arguments.executable_path.name) + ': ' + str(self.arguments.executable_path.value) + '\n\t\t\t'
             + str(self.arguments.days_to_schedule.name) + ': ' + str(self.arguments.days_to_schedule.value) + '\n\t\t\t'
             + str(self.arguments.time_to_schedule.name) + ': ' + str(self.arguments.time_to_schedule.value)
             )

    def __get_configs_from_file(self):
        list_of_configs = self.__read_yaml()
        settings = []

        for config in list_of_configs:
            arguments = ProgArguments()
            list_args = arguments.to_list()

            for arg in list_args:
                arg.set_argument_value(list_of_configs[config][arg.name])

            arguments.from_list(list_args)
            arguments.configure = self.arguments.configure
            settings.append(arguments)

        return settings

    def __process_configuration(self, configuration):
        if configuration.name not in self.original_arguments:
            if not self.is_configured():
                argument_value = configuration.default
            else:
                try:
                    argument_value = self.settings[configuration.name]
                except KeyError:
                    argument_value = configuration.default
        else:
            argument_value = getattr(self.original_arguments, configuration.name)

        configuration.set_argument_value(argument_value)
        return configuration.value

    def __write_to_file(self):
        arguments = self.arguments.to_list()
        list_of_configs = {}
        program_alias = arguments[0].value

        # open all configs from file if configured
        if self.is_configured():
            list_of_configs = self.__read_yaml()

        # create new or update where program alias is current
        list_of_configs[program_alias] = self.settings

        # open file to save new configs
        self.__write_yaml(list_of_configs)

    def __read_yaml(self):
        configs_file = self.file.open('r')
        list_of_configs = yaml.safe_load(configs_file)
        self.file.close()
        return list_of_configs

    def __write_yaml(self, list_of_configs):
        configs_file = self.file.open('w')
        yaml.safe_dump(list_of_configs, configs_file)
        self.file.close()

    def __check_deletion_of_config(self):
        try:
            if self.original_arguments.delete_schedule:
                pass

            if self.is_configured():
                list_of_configs = self.__read_yaml()

                list_of_configs.pop(self.original_arguments.delete_schedule)

                if list_of_configs:
                    self.__write_yaml(list_of_configs)
                else:
                    self.file.open('w').close()

                show('The following configuration \n\t\t\t\'' + self.original_arguments.delete_schedule + '\'\n\t\t was deleted.')

            sys.exit()

        except (AttributeError, KeyError):
            pass

    def __check_list_all_configs(self):
        try:
            if not self.original_arguments.list_all_configs:
                pass

            if self.is_configured():
                list_of_configs = self.__read_yaml()

                current_configurations_list = 'Current configurations:'
                for key in list_of_configs:
                    current_configurations_list += \
                        '\n\t\t\t' + str(list_of_configs[key]['file_alias']) + ':\n\t\t\t\t' \
                        + 'file_alias: ' + str(list_of_configs[key]['file_alias']) + '\n\t\t\t\t' \
                        + 'executable_path: ' + str(list_of_configs[key]['executable_path']) + '\n\t\t\t\t' \
                        + 'days_to_schedule: ' + str(list_of_configs[key]['days_to_schedule']) + '\n\t\t\t\t' \
                        + 'time_to_schedule: ' + str(list_of_configs[key]['time_to_schedule']) + '\n\n\t\t\t\t'

                show(current_configurations_list)
            sys.exit()
        except (AttributeError, KeyError):
            pass