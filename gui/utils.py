import os
import subprocess

from gui.api import list_configs


def reset_schedules(window):
    window['schedule'].update([alias for alias in list_configs().keys()])
    window['edit_days'].update('')
    window['edit_exclude'].update('')
    window['edit_include'].update('')
    window['edit_path'].update('')
    window['edit_status'].update('')
    window['edit_time'].update('')
    window['edit_stop'].update('')


def get_list_of_configs(values):
    if len(values['schedule']) > 0:
        return list_configs()[values['schedule'][0]]

    return {}


def check_editable_config(window, values, value_name, window_key, is_list, to_edit):
    current_values = get_list_of_configs(values)[value_name]
    input_value = window[window_key].get()

    if is_list:
        current_values = ' '.join(current_values)

    if current_values != input_value:
        if is_list:
            input_value = input_value.split(' ')
        to_edit[value_name] = [input_value, is_list]


def open_file(path):
    if os.path.exists(path):
        subprocess.Popen(r'explorer /open,"'+path+'"')
        return True

    return False


def get_icon_path():
    path = ''
    if getattr(sys, 'frozen', False):
        path = sys._MEIPASS
    return os.path.join(path, "icon\\logo.ico")
