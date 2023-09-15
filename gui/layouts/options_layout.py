import textwrap

import PySimpleGUI as sg

from gui.api import list_global_configs


def get_options_layout():

    es_text_value = 'If "ENABLE STARTUP OPTION" is selected, two folders will be opened which mean that you will need to copy the file called ' \
           '"program-scheduler.bat" to the other opened folder. '
    wrapper = textwrap.TextWrapper(width=90)
    enable_startup_help_text = wrapper.fill(text=es_text_value)

    ic_text_value = 'Any console information regarding installing the CLI will be displayed in the "RUN" tab.'
    wrapper = textwrap.TextWrapper(width=90)
    install_help_text = wrapper.fill(text=ic_text_value)

    cli_options = [
        [sg.Button('INSTALL CLI', tooltip='It will install this program\'s CLI if not installed already.')],
        [sg.Text(install_help_text)],
        [sg.Button('ENABLE STARTUP OPTION', tooltip='Disclaimer: CLI needs to be installed. Currently only available for Windows users.')],
        [sg.Text(enable_startup_help_text)],
        [sg.Button('OPEN CONFIGURATIONS FOLDER')],
        [sg.Text('', key='error_folder')],
    ]

    exit_wd = False
    if len(list_global_configs()) > 0:
        exit_wd = list_global_configs()['exit_when_done']

    return [
        [sg.Checkbox("Set exit when scheduler is done", default=exit_wd, enable_events=True, key='exit_when_done')],
        [sg.Combo(sg.theme_list(), default_value=sg.theme(), s=(15, 22), enable_events=True, readonly=True, k='-COMBO-')],
        [sg.Button('EDIT')],
        [sg.Frame('CLI Advanced Options', layout=cli_options, font='Any 8', title_color='white', expand_x=True, expand_y=True)]
    ]
