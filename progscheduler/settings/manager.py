import os

import argparse
from os.path import expanduser

from margument.non_repeatable_settings import NonRepeatableSettings
from margument.options import Options
from margument.repeatable_settings import RepeatableSettings
from margument.settings_processor import SettingsProcessor

from progscheduler.settings.generic_arguments import Generic
from progscheduler.settings.specific_arguments import Specific
from progscheduler.version.progsettings import get_version


def get_path():
    home = expanduser("~")
    path = os.path.join(home, 'progscheduler')
    if not os.path.exists(path):
        os.mkdir(path)
    final_path = os.path.join(path, 'settings')
    if not os.path.exists(final_path):
        os.mkdir(final_path)

    return final_path


class Manager:
    is_to_configure = False

    def __init__(self, is_gui):
        self.is_gui = is_gui
        self.args = argparse.ArgumentParser()
        self.args.add_argument('--version', action='version', version='%(prog)s ' + str(get_version()))

    def configure_arguments(self, custom_args):
        # manage specific configurations
        specific = Specific()
        specific.set_is_gui(self.is_gui)

        local_settings = RepeatableSettings(path=os.path.join(get_path(), 'local.yaml'),
                                            program_arguments=specific,
                                            options=Options(show_saved=True, save_main_arg_exists=True))
        specific.are_configs_saved = local_settings.exists()

        # manage generic configurations
        global_settings = NonRepeatableSettings(path=os.path.join(get_path(), 'global.yaml'),
                                                program_arguments=Generic(),
                                                options=Options(show_saved=True, save_different=True))

        settings_processor = SettingsProcessor([local_settings, global_settings], self.args)
        return settings_processor.run(custom_args)
