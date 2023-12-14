from my_settings import my_settings


class MyStatus:
    def __init__(self):
        self._use_next_half_hour = True
        self._saved_half_hour = None
        self._next_half_hour = None
        self._current_time = None
        self._force_update = True
        self._current_title = my_settings.titles.get(5)

    @property
    def use_next_half_hour(self):
        return self._use_next_half_hour

    @use_next_half_hour.setter
    def use_next_half_hour(self, value):
        # You can add any validation logic here if needed
        self._use_next_half_hour = value

    @property
    def saved_half_hour(self):
        return self._saved_half_hour

    @saved_half_hour.setter
    def saved_half_hour(self, value):
        # You can add any validation logic here if needed
        self._saved_half_hour = value

    @property
    def next_half_hour(self):
        return self._next_half_hour

    @next_half_hour.setter
    def next_half_hour(self, value):
        # You can add any validation logic here if needed
        self._next_half_hour = value

    @property
    def current_time(self):
        return self._current_time

    @current_time.setter
    def current_time(self, value):
        # You can add any validation logic here if needed
        self._current_time = value

    @property
    def force_update(self):
        return self._force_update

    @force_update.setter
    def force_update(self, value):
        # You can add any validation logic here if needed
        self._force_update = value

    @property
    def current_title(self):
        return self._current_title

    @current_title.setter
    def current_title(self, value):
        # You can add any validation logic here if needed
        self._current_title = value

