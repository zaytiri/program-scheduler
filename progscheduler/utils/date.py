from datetime import datetime, timedelta


class Date:

    def __init__(self, date='', time='', date_separator='', time_separator=''):
        self.date_str = date
        self.time_str = time
        self.date_separator = date_separator
        self.time_separator = time_separator
        self.now = datetime.now()
        self.converted_date = self.convert_date()
        self.converted_time = self.convert_time()

    def convert_date(self):
        try:
            splitted_date = self.date_str.split(self.date_separator)
            self.converted_date = datetime(
                day=int(splitted_date[0]),
                month=int(splitted_date[1]),
                year=int(splitted_date[2]),
            )
            return self.converted_date
        except ValueError:
            pass

    def convert_time(self):
        try:
            splitted_time = self.time_str.split(self.time_separator)
            self.converted_time = datetime(
                day=datetime.min.day,
                month=datetime.min.month,
                year=datetime.min.year,

                hour=int(splitted_time[0]),
                minute=int(splitted_time[1])
            )
            if len(splitted_time) == 3:
                self.converted_time += timedelta(seconds=int(splitted_time[2]))

            return self.converted_time
        except ValueError:
            pass

    def greater_than_today(self):
        if self.converted_date is None:
            return False

        if self.converted_date >= datetime.combine(datetime.today().date(), self.converted_date.time()):
            return True
        return False

    def lesser_than_today(self):
        if self.converted_date is None:
            return False

        if self.converted_date < datetime.combine(datetime.today().date(), self.converted_date.time()):
            return True
        return False

    def equals_to_today(self):
        if self.converted_date is None:
            return False

        if self.converted_date == datetime.combine(datetime.today().date(), self.converted_date.time()):
            return True
        return False

    def time_greater_than_today(self):
        if self.converted_time is None:
            return False

        self.now = datetime.now()
        if self.now.hour >= int(self.converted_time.hour) and self.now.minute >= int(self.converted_time.minute):
            return True
        return False

    @staticmethod
    def get_current_day_name():
        return datetime.now().strftime("%A").lower()
