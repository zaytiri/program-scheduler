import os
import signal
import sys
from datetime import datetime

from progscheduler.jobs import open_program
from progscheduler.settings.manager import Manager
from progscheduler.utils.log import show
from progscheduler.scheduler import Scheduler


def main():
    arguments = get_processed_arguments()

    validate(arguments)

    run_scheduler(arguments)


def get_processed_arguments():
    manager = Manager()
    return manager.configure_arguments()


def validate(arguments):
    if not arguments['Generic'].run.value:
        sys.exit()

    if arguments['Generic'].time_to_stop.value != 'off'.lower():
        now = datetime.utcnow()
        time = arguments['Generic'].time_to_stop.value.split(':')
        if now.hour >= int(time[0]) and now.minute > int(time[1]):
            show('Option: \"time-to-stop\" is enabled. Nothing will run after defined time: ' + arguments['Generic'].time_to_stop.value + '. Current '
                'time: ' + str(now.hour) + ':' + str(now.minute))
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

    # if arguments['Generic'].exit_when_done.value:
    #     exit(0)


def do_scheduled_job(scheduler, program):
    scheduler.set_method_to_schedule(lambda: open_program(program.path.value))
    scheduler.process(
        program.days.value,
        program.time.value
    )


if __name__ == '__main__':
    main()
