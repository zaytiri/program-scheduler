import PySimpleGUI as sg


def get_run_layout():
    return [
        [sg.Text('Click "RUN" to run the default scheduler for today:')],
        [sg.Multiline("",
                      autoscroll=True,
                      write_only=True,
                      auto_refresh=True,
                      disabled=True,
                      expand_x=True,
                      expand_y=True,
                      echo_stdout_stderr=True,
                      reroute_stdout=True)
         ],
        [sg.Text('', key='run_error')],
        [sg.Button('RUN')]
    ]