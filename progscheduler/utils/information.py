import sys


def show(message, to_exit=False):
    print('    >>!:\n\t\t' + message + '\n')

    if to_exit:
        sys.exit()
