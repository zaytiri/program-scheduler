import sys


def throw(message):
    print('\t>>!ERROR:\n\t\t' + message)
    sys.exit()


def show(message, to_exit=False):
    print('    >>!:\n\t\t' + message + '\n')

    if to_exit:
        sys.exit()
