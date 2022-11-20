import datetime
import os
import sys
import time
import schedule

from progscheduler.arguments import Arguments
from progscheduler.jobs import open_program
from scheduler import Scheduler


# -e "C:\Users\ziia\AppData\Local\Vivaldi\Application\vivaldi.exe" -a browser -d monday friday saturday
# -del browser


def main():
    arguments = Arguments().configure()

    if arguments[0].configure.value:
        sys.exit()

    scheduler = Scheduler()

    for program in arguments:
        process_scheduler(scheduler, program)

    scheduler.run()


def process_scheduler(scheduler, program_to_schedule):
    scheduler.set_method_to_schedule(lambda: open_program(program_to_schedule.executable_path.value))
    scheduler.process(
        program_to_schedule.days_to_schedule.value,
        program_to_schedule.time_to_schedule.value
    )


if __name__ == '__main__':
    main()
