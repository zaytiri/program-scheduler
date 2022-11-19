from progscheduler.services.directory import Directory
from entities.prog_arguments import ProgArguments
from configurations.configurations import Configurations
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

        self.args.add_argument(self.prog_arguments.root.abbreviation_name, self.prog_arguments.root.full_name,
                               required=not self.are_configs_saved,
                               help=self.prog_arguments.root.help_message,
                               metavar=self.prog_arguments.root.metavar,
                               default=argparse.SUPPRESS)

    def __check_any_errors(self):
        pass

    @staticmethod
    def __given_argument_path_exists(path):
        argument_path = Directory(path)
        return argument_path.exists()
