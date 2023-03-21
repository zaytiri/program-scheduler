import os

import argparse

from margument.non_repeatable_settings import NonRepeatableSettings
from margument.options import Options
from margument.repeatable_settings import RepeatableSettings
from margument.settings_processor import SettingsProcessor

from progscheduler.settings.generic_arguments import Generic
from progscheduler.settings.specific_arguments import Specific
from version.progsettings import get_version


class Manager:
    is_to_configure = False

    def __init__(self):
        self.args = argparse.ArgumentParser()
        self.args.add_argument('--version', action='version', version='%(prog)s ' + str(get_version()))

    def configure_arguments(self):
        # manage specific configurations
        specific = Specific()
        local_settings = RepeatableSettings(path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'local.yaml'),
                                            program_arguments=specific,
                                            options=Options(show_saved=True, save_main_arg_exists=True))
        specific.are_configs_saved = local_settings.exists()

        # manage generic configurations
        global_settings = NonRepeatableSettings(path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'global.yaml'),
                                                program_arguments=Generic(),
                                                options=Options(show_saved=True, save_different=True))

        settings_processor = SettingsProcessor([local_settings, global_settings], self.args)
        return settings_processor.run()
