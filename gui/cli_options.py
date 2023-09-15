import os
import subprocess
import sys
from os.path import expanduser

from gui.utils import open_file


def install_program():
    print('>> '+' '.join(['pip', 'install', 'progscheduler']), end='\n\n')
    process = subprocess.Popen(['pip', 'install', 'progscheduler'], stdout=subprocess.PIPE).communicate()[0]
    print(process.decode('utf-8'))


def enable_startup_option():
    file_path = os.path.join(sys._MEIPASS, 'files')
    file_destination = os.path.join(expanduser("~"), 'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    open_file(file_path)
    open_file(file_destination)


def go_to_settings_files():
    home = expanduser("~")
    path = os.path.join(home, 'progscheduler\\settings')
    return open_file(path)
