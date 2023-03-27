import argparse
from datetime import datetime

from margument.argument import Argument
from margument.arguments import Arguments

from progscheduler.utils.directory import Directory
from progscheduler.utils.log import throw, show


class Specific(Arguments):
    are_configs_saved = False

    def __init__(self):
        self.alias = Argument(name='alias',
                              abbreviation_name='-a',
                              full_name='--alias',
                              help_message='chosen UNIQUE alias for the file. when updating any configurations this flag needs to be used. this only '
                                           'works if the file path already exists in the configurations.',
                              metavar="",
                              to_save=True,
                              is_main=True)

        self.path = Argument(name='path',
                             abbreviation_name='-p',
                             full_name='--path',
                             help_message='absolute path of file to schedule.',
                             metavar="",
                             to_save=True)

        self.days = Argument(name='days',
                             abbreviation_name='-d',
                             full_name='--days',
                             help_message='days of the week for when the file will start. multiple values can be set. available set of values: '
                                          '\'monday\', \'tuesday\', \'wednesday\', \'thursday\', \'friday\', \'saturday\' and \'sunday\'.',
                             metavar="",
                             to_save=True,
                             default=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'everyday',
                                      'weekdays', 'weekends'])

        self.time = Argument(name='time',
                             abbreviation_name='-t',
                             full_name='--time',
                             help_message='input a specific time to start the file. example: \'08:15\'. default value is: \'at startup\'. If is \'at '
                                          'startup\' then the file will be scheduled to open at startup.',
                             metavar="",
                             to_save=True,
                             default='at startup')

        self.time_to_stop = Argument(name='time_to_stop',
                                     abbreviation_name='-ts',
                                     full_name='--time-to-stop',
                                     help_message='If a time is set, the scheduled job will not run, after specified time in a day. If this argument '
                                                  'equals \"off\", this setting will be ignored. Time is expected to be according to 24 hours cycle. '
                                                  'example: -ss 13:30 (meaning the job will not run if time exceeds 13:30), -ss off',
                                     metavar="",
                                     to_save=True,
                                     default='off')

        self.status = Argument(name='status',
                               abbreviation_name='-st',
                               full_name='--status',
                               help_message='This indicates if a scheduled job is active or inactive. Default value is \"on\". example -st on, '
                                            '-st off',
                               metavar="",
                               to_save=True,
                               default='on')

        self.exclude = Argument(name='exclude',
                                abbreviation_name='-ex',
                                full_name='--exclude',
                                help_message='This indicates the specific days for when a specific scheduled job will not run. Can be added multiple '
                                             'dates in the format dd/mm/yyyy. Default value is empty. example: -ex 29/03/2023 25/12/2023. [NOTE]: '
                                             'Any dates inserted will be replacing dates configured before.',
                                metavar="",
                                to_save=True,
                                default=[])

    def set_are_configs_saved(self, are_configs_saved):
        self.are_configs_saved = are_configs_saved

    def add_arguments(self, args_parser):
        args_parser.add_argument(self.path.abbreviation_name, self.path.full_name,
                                 required=not self.are_configs_saved,
                                 help=self.path.help_message,
                                 metavar=self.path.metavar,
                                 default=argparse.SUPPRESS)

        args_parser.add_argument(self.alias.abbreviation_name, self.alias.full_name,
                                 required=not self.are_configs_saved,
                                 help=self.alias.help_message,
                                 metavar=self.alias.metavar,
                                 default=argparse.SUPPRESS)

        args_parser.add_argument(self.days.abbreviation_name, self.days.full_name,
                                 required=not self.are_configs_saved,
                                 nargs='*',
                                 choices=self.days.default,
                                 help=self.days.help_message,
                                 metavar=self.days.metavar,
                                 default=argparse.SUPPRESS)

        args_parser.add_argument(self.time.abbreviation_name, self.time.full_name,
                                 type=str,
                                 help=self.time.help_message,
                                 metavar=self.time.metavar,
                                 default=argparse.SUPPRESS)

        args_parser.add_argument(self.time_to_stop.abbreviation_name, self.time_to_stop.full_name,
                                 help=self.time_to_stop.help_message,
                                 metavar=self.time_to_stop.metavar,
                                 default=argparse.SUPPRESS)

        args_parser.add_argument(self.status.abbreviation_name, self.status.full_name,
                                 choices=['on', 'off'],
                                 help=self.status.help_message,
                                 metavar=self.status.metavar,
                                 default=argparse.SUPPRESS)

        args_parser.add_argument(self.exclude.abbreviation_name, self.exclude.full_name,
                                 nargs='*',
                                 help=self.exclude.help_message,
                                 metavar=self.exclude.metavar,
                                 default=argparse.SUPPRESS)

    def process_arguments(self, settings):
        self.__validate_exclude_dates(settings[0].user_arguments)
        self.__validate_path(settings[0].user_arguments)
        self.__validate_days(settings[0].user_arguments)

    def __validate_days(self, user_arguments):
        if self.days.name in user_arguments:
            if user_arguments.days[0] == 'weekdays':
                user_arguments.days = self.__get_specific_days('weekdays')
            elif user_arguments.days[0] == 'weekends':
                user_arguments.days = self.__get_specific_days('weekends')
            elif user_arguments.days[0] == 'everyday':
                user_arguments.days = self.__get_specific_days('everyday')

    def __validate_exclude_dates(self, user_arguments):
        if self.exclude.name in user_arguments:
            for date in user_arguments.exclude:
                user_date = date.split('/')
                try:
                    validate_date = datetime(day=int(user_date[0]), month=int(user_date[1]), year=int(user_date[2]))
                    if validate_date < datetime.combine(datetime.today().date(), datetime.min.time()):
                        show('\'' + date + '\': is an old date. It will be ignored.', to_exit=True)
                except ValueError:
                    throw('\'' + date + '\': date not valid.')

    def __validate_path(self, user_arguments):
        if self.path.name in user_arguments:
            if not self.__given_argument_path_exists(user_arguments.path):
                throw('\'' + user_arguments.path + '\' path does not exist.')

    def __get_specific_days(self, days_specified):
        days = []

        if days_specified == 'weekdays':
            for i in range(0, 5):
                days.append(self.days.default[i])
            return days

        if days_specified == 'weekends':
            for i in range(5, 7):
                days.append(self.days.default[i])
            return days

        for i in range(0, 7):
            days.append(self.days.default[i])
        return days

    @staticmethod
    def __given_argument_path_exists(path):
        argument_path = Directory(path)
        return argument_path.exists()
