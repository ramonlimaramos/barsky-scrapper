from freezegun import freeze_time


__all__ = ['DateTimeMixin']


class DateTimeMixin:

    freezer = None

    def datetime_tear_down(self):
        if self.freezer is not None:
            self.freezer.stop()

    def given_today_is(self, year, month, day):
        self.freezer = freeze_time(f'{year}-{month}-{day}')
        self.freezer.start()