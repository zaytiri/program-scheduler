import textwrap

from .argument import Argument


class ProgArguments:
    """
    This class is responsible for creating an object containing all arguments used in the program
    """

    def __init__(self):
        self.root = Argument('root',
                             '-r',
                             '--root',
                             'absolute path to the following file: HandBrakeCLI.exe. example: --root \'C:\\path\\to\\folder\'',
                             "")

    def to_list(self):
        arguments = [

        ]
        return arguments

    def from_list(self, arguments):
        self.root = arguments[0]
