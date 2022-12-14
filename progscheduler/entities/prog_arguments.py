from .argument import Argument


class ProgArguments:
    """
    This class is responsible for creating an object containing all arguments used in the program
    """

    def __init__(self):
        self.file_alias = Argument('file_alias',
                                   '-a',
                                   '--file-alias',
                                   'chosen UNIQUE alias for the file. when updating any configurations this flag needs to be used. this only '
                                   'works if the file path already exists in the '
                                   'configurations.',
                                   "")

        self.executable_path = Argument('executable_path',
                                        '-e',
                                        '--executable-path',
                                        'absolute path of file to schedule.',
                                        "")

        self.days_to_schedule = Argument('days_to_schedule',
                                         '-d',
                                         '--days-to-schedule',
                                         'days of the week for when the file will start. multiple values can be set. available set of values: '
                                         '\'monday\', \'tuesday\', \'wednesday\', '
                                         '\'thursday\', \'friday\', \'saturday\' and \'sunday\'.',
                                         "",
                                         default=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'everyday',
                                                  'weekdays', 'weekends'])

        self.time_to_schedule = Argument('time_to_schedule',
                                         '-t',
                                         '--time-to-schedule',
                                         'input a specific time to start the file. example: \'08:15\'. default value is: \'at startup\'. If is \'at '
                                         'startup\' '
                                         'then the file will be scheduled to open at startup.',
                                         "",
                                         default='at startup')

        self.delete_schedule = Argument('delete_schedule',
                                        '-del',
                                        '--delete-schedule',
                                        'delete a given file alias from the scheduler. example: -d ThisNAmeRefersToCurrentProgramToSchedule',
                                        "")

        self.configure = False

    def to_list(self):
        arguments = [
            self.file_alias,
            self.executable_path,
            self.days_to_schedule,
            self.time_to_schedule,

        ]
        return arguments

    def from_list(self, arguments):
        self.file_alias = arguments[0]
        self.executable_path = arguments[1]
        self.days_to_schedule = arguments[2]
        self.time_to_schedule = arguments[3]
