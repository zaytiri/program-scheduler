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


def is_time_to_stop_valid(program_name, time_to_stop):
    if time_to_stop != 'off'.lower():
        now = datetime.utcnow()
        time = time_to_stop.split(':')
        if now.hour >= int(time[0]) and now.minute > int(time[1]):
            show('Option: \"time-to-stop\" is enabled for \'' + program_name + '\' and it will not run. Defined time: ' +
                 time_to_stop + '. Current time: ' + str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2))
            return True
    return False


def is_scheduled_today(days_to_schedule):
    now = datetime.utcnow()
    return now.strftime("%A").lower() in days_to_schedule


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
    if not is_scheduled_today(program.days.value):
        return

    if is_time_to_stop_valid(program.alias.value, program.time_to_stop.value):
        return

    scheduler.set_method_to_schedule(lambda: open_program(program.path.value))
    scheduler.process(
        program.days.value,
        program.time.value
    )


if __name__ == '__main__':
    main()
