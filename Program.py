from datetime import datetime


class Program(object):
    def __init__(self, title: str, date_time: datetime, location: str, url: str, price_str: str):
        self.title = title
        self.date_time = date_time
        self.location = location
        self.url = url
        self.price_str = price_str
