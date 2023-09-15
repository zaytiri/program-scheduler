import argparse

from margument.argument import Argument
from margument.arguments import Arguments

from progscheduler.utils.date import Date
from progscheduler.utils.directory import Directory
from progscheduler.utils.log import throw, show
from progscheduler.utils.reflection import get_class_variables, convert_to_dict


class Specific(Arguments):
    are_configs_saved = False

    def __init__(self):
        self.is_gui = None
        self.alias = Argument(name='alias',
                              abbreviation_name='-a',
                              full_name='--alias',
                              help_message='A UNIQUE alias for the file to be scheduled. When creating and/or updating any configurations, '
                                           'this alias needs to be present.',
                              metavar="",
                              to_save=True,
                              is_main=True)

        self.path = Argument(name='path',
                             abbreviation_name='-p',
                             full_name='--path',
                             help_message='Absolute path of the file to be scheduled.',
                             metavar="",
                             to_save=True,
                             default='')

        self.days = Argument(name='days',
                             abbreviation_name='-d',
                             full_name='--days',
                             help_message='Days of the week for when the scheduled job will run. Multiple values can be inserted. Following '
                                          'are the available set of values: \'monday\', \'tuesday\', \'wednesday\', \'thursday\', \'friday\', '
                                          '\'saturday\', \'sunday\', \'everyday\', \'weekdays\' and \'weekends\'. The 3 latter should be used '
                                          'individually.',
                             metavar="",
                             to_save=True,
                             default=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])

        self.time = Argument(name='time',
                             abbreviation_name='-t',
                             full_name='--time',
                             help_message='Insert a specific time to start the file. example: \'08:15\'. default value is: \'at startup\'. If is '
                                          '\'at startup\' then the file will be scheduled to open first thing when the program runs.',
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

        self.include = Argument(name='include',
                                abbreviation_name='-in',
                                full_name='--include',
                                help_message='This indicates the specific days for when a specific scheduled job should run that it wouldn\'t '
                                             'normally run. Can be added multiple dates in the format dd/mm/yyyy. Default value is empty. example: '
                                             '-in 14/03/2023 23/06/2023. [NOTE]: Any dates inserted will be replacing dates configured before.',
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
                                 nargs='*',
                                 choices=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'everyday', 'weekdays',
                                          'weekends'],
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

        args_parser.add_argument(self.include.abbreviation_name, self.include.full_name,
                                 nargs='*',
                                 help=self.include.help_message,
                                 metavar=self.include.metavar,
                                 default=argparse.SUPPRESS)

    def process_arguments(self, settings):
        self.__validate_existence_of_alias(settings[0].user_arguments)
        self.__validate_path(settings[0].user_arguments)
        self.__validate_days(settings[0].user_arguments)
        self.__validate_exclude_include_dates(settings[0].settings_from_file, settings[0].user_arguments)

    def set_is_gui(self, is_gui):
        self.is_gui = is_gui

    def __validate_existence_of_alias(self, user_arguments):
        is_configurable = False
        for var in get_class_variables(self):
            if not isinstance(var[1], Argument):
                continue

            if var[1].name in user_arguments:
                is_configurable = True

        if is_configurable and self.alias.name not in user_arguments:
            throw('An alias is needed for specific configurations.')

    def __validate_days(self, user_arguments):
        if self.days.name in user_arguments:
            if user_arguments.days[0] == 'weekdays':
                user_arguments.days = self.__get_specific_days('weekdays')
            elif user_arguments.days[0] == 'weekends':
                user_arguments.days = self.__get_specific_days('weekends')
            elif user_arguments.days[0] == 'everyday':
                user_arguments.days = self.__get_specific_days('everyday')

    def __validate_dates(self, user_list, current_dates):
        for date in user_list:
            validate_date = Date(date=date, date_separator='/')
            try:
                if validate_date.lesser_than_today():
                    show('\'' + date + '\': is an old date. Cannot be added.', to_exit=not self.is_gui)
                current_dates.append(validate_date.converted_date)
            except ValueError:
                throw('\'' + date + '\': date not valid.', to_exit=not self.is_gui)

    def __validate_exclude_include_dates(self, file, user_arguments):
        include_dates = self.__get_dates_list(file, user_arguments, self.include.name)
        exclude_dates = self.__get_dates_list(file, user_arguments, self.exclude.name)

        duplicate_dates = set(include_dates) & set(exclude_dates)
        if duplicate_dates:
            message = 'Following dates cannot exist on both exclude and include lists:'
            for dup in duplicate_dates:
                message += '\n\t\t   - ' + dup.strftime('%d/%m/%Y')
                if self.include.name in user_arguments:
                    user_arguments.include = ''
                elif self.exclude.name in user_arguments:
                    user_arguments.exclude = ''
            throw(message, to_exit=not self.is_gui)

    def __get_dates_list(self, file, user_arguments, name):
        dates = []

        if self.include.name not in user_arguments and self.exclude.name not in user_arguments:
            return dates

        if self.alias.name in user_arguments and user_arguments.alias in file:
            try:
                file_list = file[user_arguments.alias][name]
                reduced_file_list = []
                for old_date in file_list:
                    validate_date = Date(date=old_date, date_separator='/')
                    if validate_date.greater_than_today():
                        reduced_file_list.append(old_date)
                self.__validate_dates(reduced_file_list, dates)
            except KeyError:
                pass

        if name in user_arguments:
            args = convert_to_dict(user_arguments)
            self.__validate_dates(args[name], dates)

        return dates

    def __validate_path(self, user_arguments):
        if self.path.name in user_arguments:
            if not self.__given_argument_path_exists(user_arguments.path):
                throw('\'' + user_arguments.path + '\' path does not exist.', to_exit=not self.is_gui)

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
