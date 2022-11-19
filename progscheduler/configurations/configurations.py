import os
import sys

import yaml

from progscheduler.entities.prog_arguments import ProgArguments
from progscheduler.services.directory import Directory
from progscheduler.services.file import File


class Configurations:
    original_arguments = None
    arguments = ProgArguments()
    settings = {}
    path = os.path.dirname(os.path.realpath(__file__)) + '\\userconfigs.yaml'
    file = File(path)

    def set_original_arguments(self, original_arguments):
        self.original_arguments = original_arguments

    def process(self):
        self.__check_deletion_of_config()

        if self.is_configured():
            try:
                arguments = self.arguments.to_list()
                self.settings = self.__read_yaml()[arguments[0].value]
            except KeyError:
                pass

        self.__configure()

        return self.arguments

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

        self.arguments.from_list(arguments)

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

                print('config deleted.')

                sys.exit()

        except (AttributeError, KeyError):
            pass
