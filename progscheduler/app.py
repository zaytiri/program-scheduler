import os

from progscheduler.jobs import open_program
from progscheduler.settings.manager import Manager
from progscheduler.utils.date import Date
from progscheduler.utils.log import show
from progscheduler.scheduler import Scheduler


def main(custom_args=None, is_gui=False):
    arguments = get_processed_arguments(custom_args, is_gui)

    run_scheduler(arguments, is_gui)


def get_processed_arguments(custom_args, is_gui):
    manager = Manager(is_gui)
    return manager.configure_arguments(custom_args)


def validate_global_settings(arguments):
    if arguments['Generic'].exit_when_done.value:
        show('Option: \"exit-when-done\" is enabled. This windows will close automatically when all jobs are done.')


def run_scheduler(arguments, is_gui):
    validate_global_settings(arguments)

    if not arguments['Generic'].run.value:
        return

    show('The program will now start running the scheduler.\n\n\t\t\t*NOTE:* While this is running this window should not be closed. If you are '
         'certain that all scheduled jobs are already finished, then it is safe to close this window.')

    scheduler = Scheduler()

    for program in arguments['Specific']:
        do_scheduled_job(scheduler, arguments['Specific'][program])

    exit_program = arguments['Generic'].exit_when_done.value
    if is_gui:
        exit_program = is_gui

    scheduler.run(exit_program)

    if arguments['Generic'].exit_when_done.value or is_gui:
        os.system('title kill_current_terminal_window')
        os.system(f'taskkill /f /fi "WINDOWTITLE eq kill_current_terminal_window"')


def do_scheduled_job(scheduler, program):
    if not job_will_run(program):
        return

    scheduler.set_method_to_schedule(lambda: open_program(program.alias.value, program.path.value))
    scheduler.process(
        program.days.value,
        program.time.value
    )


def job_will_run(program):
    if not is_scheduled_today(program.days.value, program.alias.value, program.include.value, program.days.value, program.exclude.value):
        return False

    if is_time_to_stop(program.alias.value, program.time_to_stop.value):
        return False

    if not is_job_active(program.alias.value, program.status.value):
        return False

    return True


def is_time_to_stop(program_name, time_to_stop):
    if time_to_stop != 'off'.lower():
        validate_time = Date(time=time_to_stop, time_separator=':')
        if validate_time.time_greater_than_today():
            show('Option: \"time-to-stop\" is enabled for \'' + program_name + '\' and it will not run. Defined time: ' +
                 time_to_stop + '. Current time: ' + str(validate_time.now.hour).zfill(2) + ':' + str(validate_time.now.minute).zfill(2))
            return True
    return False


def is_scheduled_today(days_to_schedule, program_name, included_days, days, excluded_days):
    if is_included_day(program_name, included_days, days):
        return True

    if is_excluded_day(program_name, excluded_days):
        return False

    # this condition needs to be the last one
    if Date.get_current_day_name() not in days_to_schedule:
        return False

    return True


def is_job_active(program_name, status):
    if status.lower() == 'off'.lower():
        show('\"' + program_name + '\" is inactive and it will not run. Status: OFF.')
        return False
    return True


def is_excluded_day(program_name, excluded_days):
    return check_days(program_name, excluded_days, ['not', 'excluded'])


def is_included_day(program_name, included_days, days):
    if check_days(program_name, included_days, ['', 'included']):
        days.append(Date.get_current_day_name())
        return True
    return False


def check_days(program_name, days, message):
    for date in days:
        validate_date = Date(date=date, date_separator='/')
        if validate_date.equals_to_today():
            show('Today \"' + program_name + '\" will ' + message[0] + ' run. ' + validate_date.converted_date.strftime('%d/%m/%Y') + ' is an ' + message[1]
                 + ' date.')
            return True
    return False


if __name__ == '__main__':
    main()
