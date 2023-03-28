import os
from datetime import datetime

from progscheduler.utils.log import show


def open_program(name, root_path):
    if root_path == '':
        show('Following scheduled job does not have a path: ' + name)
        return

    now = datetime.now()
    os.startfile(root_path)
    show('The following file \n\t\t\t\'' + root_path + '\'\n\t\t has started at ' + str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2) + ':' + str(
        now.second).zfill(2) + '.')
