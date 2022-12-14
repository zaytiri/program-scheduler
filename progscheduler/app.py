import sys
from progscheduler.arguments import Arguments
from progscheduler.jobs import open_program
from progscheduler.utils.information import show
from scheduler import Scheduler


def main():
    arguments = Arguments().configure()

    if arguments[0].configure:
        sys.exit()

    show('The program will now start running the scheduler. While this is running this window should not be closed because that will stop the '
         'schedule. If you know that all scheduled jobs are already finished, then it is safe to close this window.')

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
