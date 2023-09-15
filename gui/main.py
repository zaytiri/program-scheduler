import webbrowser

import PySimpleGUI as sg
from gui.api import list_configs, list_global_configs, delete_config, edit_schedule, add_new_schedule, set_exit_when_done, run_scheduler
from gui.cli_options import install_program, enable_startup_option, go_to_settings_files
from gui.layouts.help_layout import get_help_layout
from gui.layouts.run_layout import get_run_layout
from gui.layouts.groups_layout import get_groups_layout
from gui.utils import reset_schedules, check_editable_config, get_icon_path
from gui.layouts.view_edit_layout import get_view_edit_layout
from gui.layouts.add_layout import get_add_layout
from gui.layouts.options_layout import get_options_layout


def make_window():
    layout = [
        [sg.TabGroup(
            [
                [
                    sg.Tab('Run', get_run_layout()),
                    sg.Tab('Groups', get_groups_layout()),
                    sg.Tab('View/Edit', get_view_edit_layout()),
                    sg.Tab('Add', get_add_layout()),
                    sg.Tab('Options', get_options_layout()),
                    sg.Tab('Help', get_help_layout())
                ]
            ])
        ]
    ]

    win = sg.Window('Program Scheduler', layout, finalize=True, icon=get_icon_path())

    return win


window = make_window()

weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
weekends = ['saturday', 'sunday']

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if values['-COMBO-'] != sg.theme():
        sg.theme(values['-COMBO-'])
        window.close()
        window = make_window()

    if event == 'RUN':
        if len(list_configs()) == 0:
            window['run_error'].update('ERROR: No configurations are available. Please add a new schedule.')
            continue
        run_scheduler()

    if event == 'ADD' and values['new_alias'] != '' and values['new_path'] != '':
        add_new_schedule(values['new_path'], values['new_alias'])
        reset_schedules(window)
        window['new_path'].update('')
        window['new_alias'].update('')

    if event == 'SAVE':
        set_exit_when_done(values['exit_when_done'])
        window['exit_when_done'].update(list_global_configs()['exit_when_done'])

    if event == 'DELETE':
        delete_config(values['schedule'][0])
        reset_schedules(window)

    if event == 'EDIT':
        to_edit = {}

        check_editable_config(window, values, 'days', 'edit_days', True, to_edit)
        check_editable_config(window, values, 'exclude', 'edit_exclude', True, to_edit)
        check_editable_config(window, values, 'include', 'edit_include', True, to_edit)
        check_editable_config(window, values, 'path', 'edit_path', False, to_edit)
        check_editable_config(window, values, 'status', 'edit_status', False, to_edit)
        check_editable_config(window, values, 'time', 'edit_time', False, to_edit)
        check_editable_config(window, values, 'time_to_stop', 'edit_stop', False, to_edit)

        edit_schedule(values['schedule'][0], to_edit)
        reset_schedules(window)

    if event == 'STARTUP':
        window['edit_time'].update('at startup')

    if event == 'OFF':
        window['edit_stop'].update('off')

    if event == 'INSTALL CLI':
        install_program()

    if event == 'ENABLE STARTUP OPTION':
        enable_startup_option()

    if event == 'OPEN CONFIGURATIONS FOLDER' and not go_to_settings_files():
        window['error_folder'].update('ERROR: The settings folder does not exist yet. Add new Schedules.')

    if event.startswith("URL "):
        url = event.split(' ')[1]
        webbrowser.open(url)

    if event == 'choice_days':
        if values['choice_days'] == 'everyday':
            window['edit_days'].update(' '.join(weekdays + weekends))
        elif values['choice_days'] == 'weekdays':
            window['edit_days'].update(' '.join(weekdays))
        elif values['choice_days'] == 'weekends':
            window['edit_days'].update(' '.join(weekends))

    if event == 'schedule' and len(values['schedule']) > 0:
        current_values = list_configs()[values['schedule'][0]]
        window['edit_days'].update(' '.join(current_values['days']))
        window['edit_exclude'].update(' '.join(current_values['exclude']))
        window['edit_include'].update(' '.join(current_values['include']))
        window['edit_path'].update(current_values['path'])
        window['edit_status'].update(current_values['status'])
        window['edit_time'].update(current_values['time'])
        window['edit_stop'].update(current_values['time_to_stop'])

window.close()
