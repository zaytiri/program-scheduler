from progscheduler.jobs import open_program
from progscheduler.settings.manager import Manager
from progscheduler.utils.log import show
from scheduler import Scheduler


def main():
    manager = Manager()
    arguments = manager.configure_arguments()

    show('The program will now start running the scheduler. While this is running this window should not be closed because that will stop the '
         'schedule. If you know that all scheduled jobs are already finished, then it is safe to close this window.')

    scheduler = Scheduler()

    for program in arguments['Specific']:
        process_scheduler(scheduler, arguments['Specific'][program])

    scheduler.run(arguments['Generic'].exit_when_done.value)


def process_scheduler(scheduler, program):
    scheduler.set_method_to_schedule(lambda: open_program(program.path.value))
    scheduler.process(
        program.days.value,
        program.time.value
    )

# def define_method_to_schedule(program):
#     program.job


if __name__ == '__main__':
    main()
