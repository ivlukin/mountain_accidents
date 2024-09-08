from datetime import datetime


class RangersAccident:
    county = ""
    place = ""
    when = datetime.now()
    what = ""

    def __init__(self, county, place, when, what):
        self.county = county
        self.place = place
        self.when = when
        self.what = what

    def __str__(self):
        return "{0}*{1}*{2}*{3}".format(self.county, self.place, self.when, self.what)