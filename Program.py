from datetime import datetime


class Program(object):
    def __init__(self, title: str, date_time: datetime, location: str, url: str):
        self.title = title
        self.date_time = date_time
        self.location = location
        self.url = url
