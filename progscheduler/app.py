import datetime
import os
import sys
import time
import schedule

from progscheduler.arguments import Arguments
from scheduler import Scheduler


def main():
    # arguments = Arguments().configure()

    root_path = 'C:\\Users\\ziia\\AppData\\Local\\Vivaldi\\Application\\vivaldi'
    days_to_schedule = ['monday', 'friday', 'saturday']
    now = datetime.datetime.utcnow()
    time_to_schedule = '16:35'

    scheduler = Scheduler(lambda: open_program(root_path))

    scheduler.process(days_to_schedule, time_to_schedule)


def open_program(root_path):
    print('program opened')
    os.startfile(root_path)


if __name__ == '__main__':
    main()
