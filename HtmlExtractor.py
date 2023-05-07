from bs4 import BeautifulSoup
from urllib import request
from datetime import datetime
import re

from Program import Program


class HtmlExtractor(object):
    def __init__(self):
        self.date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        self.time_pattern = re.compile(r'\d{2}:\d{2}')
        self.location = '예술의전당'

    def download_html_to_soup(self, url: str) -> BeautifulSoup:
        with request.urlopen(url) as f:
            return BeautifulSoup(f.read(), 'html5lib')

    def get_program_from_url(self, url: str) -> Program:
        soup = self.download_html_to_soup(url)

        top_view = soup.find(attrs={'class': 'area show-view-top clearfix'})

        title = top_view.find(attrs={'class': 'title'}).text.strip()

        items = top_view.find(name='dt').find(name='ul').find_all(name='li')
        item_dict = dict([
            map(lambda x: x.text.strip(), list_item.find_all(name='span'))
            for list_item in items
        ])

        date_str = self.date_pattern.findall(item_dict['기간'])[0]
        time_str = self.time_pattern.findall(item_dict['시간'])[0]

        date_time = datetime.strptime(
            f'{date_str} {time_str}', '%Y-%m-%d %H:%M')

        return Program(
            title,
            date_time,
            self.location,
            url,
        )

    def get_programs_from_urls(self, urls: list[str]) -> list[Program]:
        return list(map(
            lambda url: self.get_program_from_url(url), urls
        ))
