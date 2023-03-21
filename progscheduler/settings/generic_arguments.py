import argparse

from margument.argument import Argument
from margument.arguments import Arguments

from progscheduler.settings.commands import Commands


class Generic(Arguments):
    def __init__(self):
        self.list_configs = Argument(name='list_configs',
                                     abbreviation_name='-all',
                                     full_name='--list-configs',
                                     help_message='list all existent saved configurations. example: -all',
                                     metavar="",
                                     command=Commands.get_configs)

        self.time_to_stop = Argument(name='time_to_stop',
                                     abbreviation_name='-ts',
                                     full_name='--time-to-stop',
                                     help_message='If a time is set, after this time, the scheduler will not automatically run when rebooting the '
                                                  'device. If this argument equals \"off\", this setting will be ignored. example: -ss 13:30, '
                                                  '-ss off',
                                     metavar="",
                                     to_save=True,
                                     default='off')

        self.exit_when_done = Argument(name='exit_when_done',
                                       abbreviation_name='',
                                       full_name='--exit-when-done',
                                       help_message='will exit the program when all jobs are done for the current day. the configuration will be '
                                                    'saved. example: True: --exit | False: --no-exit',
                                       metavar="",
                                       to_save=True,
                                       default=False)

        self.delete = Argument(name='delete',
                               abbreviation_name='-del',
                               full_name='--delete',
                               help_message='delete a given file alias from the scheduler. example: -d ThisNameRefersToCurrentProgramToSchedule',
                               metavar="",
                               command=Commands.delete_config)

    def add_arguments(self, args_parser):
        args_parser.add_argument(self.list_configs.abbreviation_name, self.list_configs.full_name,
                                 action='store_true',
                                 help=self.list_configs.help_message,
                                 default=argparse.SUPPRESS)

        args_parser.add_argument(self.time_to_stop.abbreviation_name, self.time_to_stop.full_name,
                                 help=self.time_to_stop.help_message,
                                 metavar=self.time_to_stop.metavar,
                                 default=argparse.SUPPRESS)

        args_parser.add_argument(self.exit_when_done.full_name,
                                 action=argparse.BooleanOptionalAction,
                                 help=self.exit_when_done.help_message,
                                 metavar=self.exit_when_done.metavar,
                                 default=argparse.SUPPRESS)

        args_parser.add_argument(self.delete.abbreviation_name, self.delete.full_name,
                                 help=self.delete.help_message,
                                 metavar=self.delete.metavar,
                                 default=argparse.SUPPRESS)

    def process_arguments(self, settings):
        self.list_configs.set_command_args(settings[0].file.path)
        self.delete.set_command_args((settings[0].user_arguments, settings[0].file.path))
