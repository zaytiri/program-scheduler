import os
import sys

import yaml


def get_version():
    if getattr(sys, 'frozen', False):
        path = os.path.join(sys._MEIPASS, "files/progsettings.yaml")
    else:
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'progsettings.yaml')

    with open(path, 'r') as settings_file:
        settings = yaml.safe_load(settings_file)['prog'.upper()]
        return settings['version'.upper()]
