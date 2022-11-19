from progscheduler.services.directory import Directory
from entities.prog_arguments import ProgArguments
from configurations.configurations import Configurations
from progscheduler.utils.error import throw
from utils.progsettings import get_version
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

        self.__check_any_errors()

        config_file.set_original_arguments(self.original_arguments)

        return config_file.process()

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

        self.args.add_argument(self.prog_arguments.program_alias.abbreviation_name, self.prog_arguments.program_alias.full_name,
                               required=not self.are_configs_saved,
                               help=self.prog_arguments.program_alias.help_message,
                               metavar=self.prog_arguments.program_alias.metavar,
                               default=argparse.SUPPRESS)

        self.args.add_argument(self.prog_arguments.days_to_schedule.abbreviation_name, self.prog_arguments.days_to_schedule.full_name,
                               required=not self.are_configs_saved,
                               nargs='*',
                               choices=self.prog_arguments.days_to_schedule.default,
                               help=self.prog_arguments.days_to_schedule.help_message,
                               metavar=self.prog_arguments.days_to_schedule.metavar,
                               default=self.prog_arguments.days_to_schedule.default)

        self.args.add_argument(self.prog_arguments.time_to_schedule.abbreviation_name, self.prog_arguments.time_to_schedule.full_name,
                               help=self.prog_arguments.time_to_schedule.help_message,
                               metavar=self.prog_arguments.time_to_schedule.metavar,
                               default=self.prog_arguments.time_to_schedule.default)

        self.args.add_argument(self.prog_arguments.delete_schedule.abbreviation_name, self.prog_arguments.delete_schedule.full_name,
                               help=self.prog_arguments.delete_schedule.help_message,
                               metavar=self.prog_arguments.delete_schedule.metavar,
                               default=argparse.SUPPRESS)

    def __check_any_errors(self):
        try:
            if not self.__given_argument_path_exists(self.original_arguments.executable_path):
                throw(self.original_arguments.executable_path + '\' path does not exist.')
        except (AttributeError, TypeError):
            pass

    @staticmethod
    def __given_argument_path_exists(path):
        argument_path = Directory(path)
        return argument_path.exists()
