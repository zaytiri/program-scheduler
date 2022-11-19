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

    scheduler = Scheduler(lambda: open_program(arguments.executable_path))

    scheduler.process(arguments.days_to_schedule, arguments.time_to_schedule)


if __name__ == '__main__':
    main()
