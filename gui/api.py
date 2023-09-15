import os
from os.path import expanduser

from progscheduler.app import main
from progscheduler.settings.commands import Commands


def run_scheduler():
    __run(['--run'])


def set_exit_when_done(set_exit):
    exit_when_done = '--exit-when-done'
    if not set_exit:
        exit_when_done = '--no-exit-when-done'
    __run([exit_when_done])


def add_new_schedule(path, alias):
    __run(['-p', path, '-a', alias])


def edit_schedule(alias, to_edit):
    args = ['-a', alias]

    for key in to_edit.keys():
        args.append('--' + key)

        if to_edit[key][1]:
            for v in to_edit[key][0]:
                args.append(v)
        else:
            args.append(to_edit[key][0])

    __run(args)


def list_configs():
    home = expanduser("~")
    file_path = os.path.join(home, 'progscheduler\\settings\\local.yaml')
    cmds = Commands().get_configs(file_path, show_input=False)
    return cmds


def list_global_configs():
    home = expanduser("~")
    file_path = os.path.join(home, 'progscheduler\\settings\\global.yaml')
    cmds = Commands().get_global_configs(file_path, show_input=False)
    return cmds


def delete_config(config):
    __run(['--delete', config])


def __run(args):
    main(args, is_gui=True)
