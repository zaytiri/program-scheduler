import textwrap

from .argument import Argument


class ProgArguments:
    """
    This class is responsible for creating an object containing all arguments used in the program
    """

    def __init__(self):
        self.program_alias = Argument('program_alias',
                                      '-a',
                                      '--program-alias',
                                      'chosen UNIQUE alias for the program. when updating any configurations for a program, this alias can be used '
                                      'instead of the whole executable path. this only works if the executable path already exists in the '
                                      'configurations.',
                                      "")

        self.executable_path = Argument('executable_path',
                                        '-e',
                                        '--executable-path',
                                        'absolute path of executable to schedule.',
                                        "")

        self.days_to_schedule = Argument('days_to_schedule',
                                         '-d',
                                         '--days-to-schedule',
                                         'days of the week for when the program will start. multiple values can be set. available set of values: '
                                         '\'monday\', \'tuesday\', \'wednesday\', '
                                         '\'thursday\', \'friday\', \'saturday\' and \'sunday\'.',
                                         "",
                                         default=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])

        self.time_to_schedule = Argument('time_to_schedule',
                                         '-t',
                                         '--time-to-schedule',
                                         'input a specific time to start the program. example: \'08:15\'. default value is empty: \'\'',
                                         "",
                                         default='')

        self.delete_schedule = Argument('delete_schedule',
                                        '-del',
                                        '--delete-schedule',
                                        'delete a given program alias from the scheduler. example: -d browser',
                                        "")

        self.configure = Argument('configure',
                                  '',
                                  '--configure',
                                  'to update or create a config, this flag needs to be enabled. default is disabled. example: --no-configure ('
                                  'disable) | --configure (enable)',
                                  "",
                                  default=False)

    def to_list(self):
        arguments = [
            self.program_alias,
            self.executable_path,
            self.days_to_schedule,
            self.time_to_schedule,

        ]
        return arguments

    def from_list(self, arguments):
        self.program_alias = arguments[0]
        self.executable_path = arguments[1]
        self.days_to_schedule = arguments[2]
        self.time_to_schedule = arguments[3]
