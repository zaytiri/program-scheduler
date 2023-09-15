import textwrap

import PySimpleGUI as sg


def get_add_layout():
    value = 'Add a new schedule by providing an "alias" and a "path". To edit other settings just use the "View/Edit" tab after ' \
                 'creation.'
    wrapper = textwrap.TextWrapper(width=100)
    add_text = wrapper.fill(text=value)

    add_config_layout = [
        [sg.Text(add_text)],
        [sg.Text('alias', size=(5, 1)), sg.Input(key='new_alias', expand_x=True)],
        [sg.Text('path', size=(5, 1)), sg.Input(key='new_path', expand_x=True), sg.FileBrowse()],
        [sg.Button('ADD')]
    ]

    return [
        [sg.Frame('Add New Schedule', add_config_layout, font='Any 8', title_color='white', expand_x=True)]
    ]