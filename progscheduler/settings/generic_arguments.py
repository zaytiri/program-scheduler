import argparse

from margument.argument import Argument
from margument.arguments import Arguments

from progscheduler.settings.commands import Commands


class Generic(Arguments):
    def __init__(self):
        self.schedules = Argument(name='schedules',
                                  abbreviation_name='-lsch',
                                  full_name='--schedules',
                                  help_message='list all saved scheduled jobs. example: -lsch',
                                  metavar="",
                                  command=Commands.get_configs,
                                  default=False)

        self.settings = Argument(name='settings',
                                 abbreviation_name='-ls',
                                 full_name='--settings',
                                 help_message='list all saved global settings. example: -ls',
                                 metavar="",
                                 command=Commands.get_global_configs,
                                 default=False)

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

        self.run = Argument(name='run',
                            abbreviation_name='-r',
                            full_name='--run',
                            help_message='if specified will run the scheduler.',
                            metavar="",
                            default=False)

    def add_arguments(self, args_parser):
        args_parser.add_argument(self.schedules.abbreviation_name, self.schedules.full_name,
                                 action='store_true',
                                 help=self.schedules.help_message,
                                 default=argparse.SUPPRESS)

        args_parser.add_argument(self.settings.abbreviation_name, self.settings.full_name,
                                 action='store_true',
                                 help=self.settings.help_message,
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

        args_parser.add_argument(self.run.abbreviation_name, self.run.full_name,
                                 action='store_true',
                                 help=self.run.help_message,
                                 default=argparse.SUPPRESS)

    def process_arguments(self, settings):
        self.schedules.set_command_args(settings[0].file.path)
        self.settings.set_command_args(settings[1].file.path)
        self.delete.set_command_args((settings[0].user_arguments, settings[0].file))
