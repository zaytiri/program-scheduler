from datetime import datetime

import schedule


class Scheduler:
    everyday = 'everyday'
    monday = 'monday'
    tuesday = 'tuesday'
    wednesday = 'wednesday'
    thursday = 'thursday'
    friday = 'friday'
    saturday = 'saturday'
    sunday = 'sunday'

    _enabled_days_of_week = {
        monday: False,
        tuesday: False,
        wednesday: False,
        thursday: False,
        friday: False,
        saturday: False,
        sunday: False
    }

    def __init__(self, method_to_schedule):
        self._method_to_schedule = method_to_schedule

    def process(self, list_of_days_to_enable, time_to_schedule=''):
        self._enable_days_of_week(list_of_days_to_enable)

        if time_to_schedule == '':
            time_to_schedule = self._get_now_date()

        if self.is_every_day_enable():
            self._do_every_day(time_to_schedule)
        else:
            self._do_specific_days(time_to_schedule)

        print(self._enabled_days_of_week)

        while True:
            schedule.run_pending()

    def is_every_day_enable(self):
        for day in self._enabled_days_of_week:
            if not self._enabled_days_of_week[day]:
                return False
        return True

    def _enable_days_of_week(self, list_of_days_to_enable):
        for day in list_of_days_to_enable:
            self._enabled_days_of_week[day] = True

    def _do_every_day(self, time_to_schedule):
        self._schedule_method(time_to_schedule, self.everyday)

    def _do_specific_days(self, time_to_schedule):
        for day in self._enabled_days_of_week:
            if self._enabled_days_of_week[day]:
                self._schedule_method(time_to_schedule, day)

    def _schedule_method(self, time_to_schedule, day='everyday'):
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

        scheduler = scheduler.at(time_to_schedule).do(self._method_to_schedule)

    @staticmethod
    def _get_now_date():
        now = datetime.utcnow()
        return str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2) + ':' + str(now.second + 1).zfill(2)
