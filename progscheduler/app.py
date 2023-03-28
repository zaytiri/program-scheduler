import os
import sys
from datetime import datetime

from progscheduler.jobs import open_program
from progscheduler.settings.manager import Manager
from progscheduler.utils.log import show
from progscheduler.scheduler import Scheduler


def main():
    arguments = get_processed_arguments()

    validate_global_settings(arguments)

    run_scheduler(arguments)


def get_processed_arguments():
    manager = Manager()
    return manager.configure_arguments()


def validate_global_settings(arguments):
    if not arguments['Generic'].run.value:
        sys.exit()

    if arguments['Generic'].exit_when_done.value:
        show('Option: \"exit-when-done\" is enabled. This windows will close automatically when all jobs are done.')


def run_scheduler(arguments):
    show('The program will now start running the scheduler.\n\n\t\t\t*NOTE:* While this is running this window should not be closed. If you are '
         'certain that all scheduled jobs are already finished, then it is safe to close this window.')

    scheduler = Scheduler()

    for program in arguments['Specific']:
        do_scheduled_job(scheduler, arguments['Specific'][program])

    scheduler.run(arguments['Generic'].exit_when_done.value)

    if arguments['Generic'].exit_when_done.value:
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
        now = datetime.now()
        time = time_to_stop.split(':')
        if now.hour >= int(time[0]) and now.minute > int(time[1]):
            show('Option: \"time-to-stop\" is enabled for \'' + program_name + '\' and it will not run. Defined time: ' +
                 time_to_stop + '. Current time: ' + str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2))
            return True
    return False


def is_scheduled_today(days_to_schedule, program_name, included_days, days, excluded_days):
    if is_included_day(program_name, included_days, days):
        return True

    if is_excluded_day(program_name, excluded_days):
        return False

    # this condition needs to be the last one
    if datetime.now().strftime("%A").lower() not in days_to_schedule:
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
        days.append(datetime.now().strftime("%A").lower())
        return True
    return False


def check_days(program_name, days, message):
    for date in days:
        saved_date = date.split('/')
        validate_date = datetime(
            day=int(saved_date[0]),
            month=int(saved_date[1]),
            year=int(saved_date[2])
        )
        if validate_date == datetime.combine(datetime.today().date(), datetime.min.time()):
            show('Today \"' + program_name + '\" will ' + message[0] + ' run. ' + validate_date.strftime('%d/%m/%Y') + ' is an ' + message[1] + ' date.')
            return True
    return False


if __name__ == '__main__':
    main()
