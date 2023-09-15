import PySimpleGUI as sg

from gui.api import list_configs


def get_view_edit_layout():
    days_choices = ['everyday', 'weekends', 'weekdays']
    viewer_layout = [
        [
            sg.Text('days', size=(10, 1)),
            sg.Input('', key='edit_days', expand_x=True),
            sg.Combo(days_choices, key='choice_days', default_value=days_choices[0], enable_events=True)
        ],
        [
            sg.Text('exclude', tooltip='input the specific days to exclude in this schedule. e.g. dd/mm/yyyy', size=(10, 1)),
            sg.Input('', key='edit_exclude', expand_x=True)
        ],
        [
            sg.Text('include', tooltip='input the specific days to include in this schedule. e.g. dd/mm/yyyy', size=(10, 1)),
            sg.Input('', key='edit_include', expand_x=True)
        ],
        [
            sg.Text('path', size=(10, 1)),
            sg.Input('', key='edit_path', expand_x=True),
            sg.FileBrowse()
        ],
        [
            sg.Text('status', size=(10, 1)),
            sg.Combo(['on', 'off'], key='edit_status', default_value='')
        ],
        [
            sg.Text('time', tooltip='input the time this scheduler should start.', size=(10, 1)),
            sg.Input('', key='edit_time', expand_x=True),
            sg.Button('STARTUP')
        ],
        [
            sg.Text('time_to_stop', tooltip='input the time after this scheduler should not run.', size=(10, 1)),
            sg.Input('', key='edit_stop', expand_x=True),
            sg.Button('OFF')
        ],
    ]

    view_configs_layout = [
        [sg.Text('View current define schedules and their details:')],
        [
            sg.Listbox([alias for alias in list_configs().keys()], enable_events=True, key='schedule', horizontal_scroll=True, size=(10, 10),
                       expand_x=True),
            sg.Frame('View/Edit', viewer_layout, font='Any 8', title_color='white', expand_x=True),
        ],
        [sg.Button('EDIT'), sg.Button('DELETE')]
    ]

    return [
        [sg.Frame('Existing Schedules', view_configs_layout, font='Any 8', title_color='white', expand_x=True)]
    ]