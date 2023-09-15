import sys


def throw(message, to_exit=False):
    print('\t>>!ERROR:\n\t\t' + message)
    if to_exit:
        sys.exit()


def show(message, to_exit=False):
    print('    >>!:\n\t' + message + '\n')
    if to_exit:
        sys.exit()
