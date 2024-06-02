from datetime import datetime


class Program(object):
    def __init__(self, title: str, date_time: datetime, date_range: list[datetime], location: str, url: str, price_str: str):
        self.title = title
        self.date_time = date_time
        self.date_range = date_range
        self.location = location
        self.url = url
        self.price_str = price_str
