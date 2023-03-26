from datetime import datetime, timedelta

import schedule


class Scheduler:
    __method_to_schedule = None
    __seconds_delay = 0

    everyday = 'everyday'
    monday = 'monday'
    tuesday = 'tuesday'
    wednesday = 'wednesday'
    thursday = 'thursday'
    friday = 'friday'
    saturday = 'saturday'
    sunday = 'sunday'

    __enabled_days_of_week = {
        monday: False,
        tuesday: False,
        wednesday: False,
        thursday: False,
        friday: False,
        saturday: False,
        sunday: False
    }

    def set_method_to_schedule(self, method_to_schedule):
        self.__method_to_schedule = method_to_schedule

    def process(self, list_of_days_to_enable, time_to_schedule):
        self.__enable_days_of_week(list_of_days_to_enable)

        if time_to_schedule == 'at startup':
            time_to_schedule = self.__get_now_date()

        if self.__is_every_day_enable():
            self.__do_every_day(time_to_schedule)
        else:
            self.__do_specific_days(time_to_schedule)

    def run(self, will_exit):
        while True:
            schedule.run_pending()
            if will_exit and self.__all_jobs_done():
                break

    @staticmethod
    def __all_jobs_done():
        for job in schedule.jobs:
            if job.next_run.day == datetime.utcnow().day:
                return False
        return True

    def __is_every_day_enable(self):
        for day in self.__enabled_days_of_week:
            if not self.__enabled_days_of_week[day]:
                return False
        return True

    def __enable_days_of_week(self, list_of_days_to_enable):
        self.__reset_enabled_days_of_week()
        for day in list_of_days_to_enable:
            self.__enabled_days_of_week[day] = True

    def __reset_enabled_days_of_week(self):
        for day in self.__enabled_days_of_week:
            self.__enabled_days_of_week[day] = False

    def __do_every_day(self, time_to_schedule):
        self.__schedule_method(time_to_schedule, self.everyday)

    def __do_specific_days(self, time_to_schedule):
        for day in self.__enabled_days_of_week:
            if self.__enabled_days_of_week[day]:
                self.__schedule_method(time_to_schedule, day)

    def __schedule_method(self, time_to_schedule, day='everyday'):
        scheduler = schedule.every()

        match day:
            case self.everyday:
                scheduler = scheduler.day
            case self.monday:
                scheduler = scheduler.monday
            case self.tuesday:
                scheduler = scheduler.tuesday
            case self.wednesday:
                scheduler = scheduler.wednesday
            case self.thursday:
                scheduler = scheduler.thursday
            case self.friday:
                scheduler = scheduler.friday
            case self.saturday:
                scheduler = scheduler.saturday
            case self.sunday:
                scheduler = scheduler.sunday

        scheduler.at(time_to_schedule).do(self.__method_to_schedule)

    def __get_now_date(self):
        self.__seconds_delay += 1
        now = datetime.now() + timedelta(seconds=self.__seconds_delay)
        return str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2) + ':' + str(now.second).zfill(2)
