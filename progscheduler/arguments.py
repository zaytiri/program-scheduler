from progscheduler.services.directory import Directory
from progscheduler.entities.prog_arguments import ProgArguments
from progscheduler.configurations.configurations import Configurations
from progscheduler.utils.error import throw
from progscheduler.utils.progsettings import get_version
import argparse


class Arguments:
    """
    This class is responsible for configuring all arguments required for the program to work including saving all mandatory argument values in a
    configuration file for easy frequent use. This way the user only has to configure the first time it runs the program or if the configuration
    file does not exist.
    """

    def __init__(self):
        self.args = None
        self.original_arguments = None
        self.prog_arguments = ProgArguments()
        self.are_configs_saved = False
        self.to_configure = False

    def configure(self):
        """
        create and configure arguments to save in a configuration file
        :return: returns all arguments either from the command line or saved configuration file
        """

        self.args = argparse.ArgumentParser()

        config_file = Configurations()

        self.are_configs_saved = config_file.is_configured()

        self.__add_arguments()

        self.original_arguments = self.args.parse_args()

        self.__check_arguments()

        self.__check_any_errors()

        config_file.set_original_arguments(self.original_arguments)

        return config_file.process(self.to_configure)

    def __add_arguments(self):
        """
        configures and adds the arguments required for the program
        """
        self.args.add_argument('--version', action='version', version='%(prog)s ' + get_version())

        self.args.add_argument(self.prog_arguments.executable_path.abbreviation_name, self.prog_arguments.executable_path.full_name,
                               required=not self.are_configs_saved,
                               help=self.prog_arguments.executable_path.help_message,
                               metavar=self.prog_arguments.executable_path.metavar,
                               default=argparse.SUPPRESS)

        self.args.add_argument(self.prog_arguments.file_alias.abbreviation_name, self.prog_arguments.file_alias.full_name,
                               required=not self.are_configs_saved,
                               help=self.prog_arguments.file_alias.help_message,
                               metavar=self.prog_arguments.file_alias.metavar,
                               default=argparse.SUPPRESS)

        self.args.add_argument(self.prog_arguments.days_to_schedule.abbreviation_name, self.prog_arguments.days_to_schedule.full_name,
                               required=not self.are_configs_saved,
                               nargs='*',
                               choices=self.prog_arguments.days_to_schedule.default,
                               help=self.prog_arguments.days_to_schedule.help_message,
                               metavar=self.prog_arguments.days_to_schedule.metavar,
                               default=argparse.SUPPRESS)

        self.args.add_argument(self.prog_arguments.time_to_schedule.abbreviation_name, self.prog_arguments.time_to_schedule.full_name,
                               type=str,
                               help=self.prog_arguments.time_to_schedule.help_message,
                               metavar=self.prog_arguments.time_to_schedule.metavar,
                               default=self.prog_arguments.time_to_schedule.default)

        self.args.add_argument(self.prog_arguments.list_all_configs.abbreviation_name, self.prog_arguments.list_all_configs.full_name,
                               action='store_true',
                               help=self.prog_arguments.list_all_configs.help_message,
                               default=argparse.SUPPRESS)

        self.args.add_argument(self.prog_arguments.delete_schedule.abbreviation_name, self.prog_arguments.delete_schedule.full_name,
                               help=self.prog_arguments.delete_schedule.help_message,
                               metavar=self.prog_arguments.delete_schedule.metavar,
                               default=argparse.SUPPRESS)

    def __check_arguments(self):
        if self.prog_arguments.file_alias.name in self.original_arguments:
            self.to_configure = True

        if self.prog_arguments.days_to_schedule.name in self.original_arguments:
            every_day_of_week = self.prog_arguments.days_to_schedule.default
            if self.original_arguments.days_to_schedule[0] == 'everyday':
                self.original_arguments.days_to_schedule = self.get_specific_days('everyday', every_day_of_week)
            elif self.original_arguments.days_to_schedule[0] == 'weekdays':
                self.original_arguments.days_to_schedule = self.get_specific_days('weekdays', every_day_of_week)
            elif self.original_arguments.days_to_schedule[0] == 'weekends':
                self.original_arguments.days_to_schedule = self.get_specific_days('weekends', every_day_of_week)

    def __check_any_errors(self):
        try:
            if not self.__given_argument_path_exists(self.original_arguments.executable_path):
                throw(self.original_arguments.executable_path + '\' path does not exist.')
        except (AttributeError, TypeError):
            pass

    @staticmethod
    def get_specific_days(days, full_list_of_days):
        if days == 'weekdays':
            full_list_of_days.pop(full_list_of_days.index('saturday'))
            full_list_of_days.pop(full_list_of_days.index('sunday'))
        elif days == 'weekends':
            full_list_of_days.pop(full_list_of_days.index('monday'))
            full_list_of_days.pop(full_list_of_days.index('tuesday'))
            full_list_of_days.pop(full_list_of_days.index('wednesday'))
            full_list_of_days.pop(full_list_of_days.index('thursday'))
            full_list_of_days.pop(full_list_of_days.index('friday'))

        full_list_of_days.pop(full_list_of_days.index('everyday'))
        full_list_of_days.pop(full_list_of_days.index('weekdays'))
        full_list_of_days.pop(full_list_of_days.index('weekends'))

        return full_list_of_days

    @staticmethod
    def __given_argument_path_exists(path):
        argument_path = Directory(path)
        return argument_path.exists()
