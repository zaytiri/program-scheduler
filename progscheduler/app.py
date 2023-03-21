import sys

from progscheduler.jobs import open_program
from progscheduler.settings.manager import Manager
from scheduler import Scheduler


def main():
    manager = Manager()
    arguments = manager.configure_arguments()
    sys.exit()

    if manager.is_to_configure:
        sys.exit()

    show('The program will now start running the scheduler. While this is running this window should not be closed because that will stop the '
         'schedule. If you know that all scheduled jobs are already finished, then it is safe to close this window.')

    scheduler = Scheduler()

    for program in arguments:
        process_scheduler(scheduler, program)

    scheduler.run(arguments[1].exit.value)


def process_scheduler(scheduler, program_to_schedule):
    scheduler.set_method_to_schedule(lambda: open_program(program_to_schedule.executable_path.value))
    scheduler.process(
        program_to_schedule.days.value,
        program_to_schedule.time.value
    )

# def define_method_to_schedule(program):
#     program.job


if __name__ == '__main__':
    main()
