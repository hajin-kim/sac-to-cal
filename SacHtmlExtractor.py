from bs4 import BeautifulSoup
from urllib import request
from datetime import datetime
import re

from Program import Program


class SacHtmlExtractor(object):
    def __init__(self):
        self.date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
        self.time_pattern = re.compile(r"\d{2}:\d{2}")
        self.price_pattern = re.compile(r"\d[\d,]*")
        self.location = "예술의전당"

    def download_html_to_soup(self, url: str) -> BeautifulSoup:
        with request.urlopen(url) as f:
            return BeautifulSoup(f.read(), "html5lib")

    def get_program_from_url(self, url: str) -> Program:
        soup = self.download_html_to_soup(url)

        top_view = soup.find(attrs={"class": "area show-view-top clearfix"})

        title = " ".join(
            top_view.find(attrs={"class": "title"})
            .text.strip()
            .replace("\n", ": ")
            .split()
        )

        items = top_view.find(name="dt").find(name="ul").find_all(name="li")
        item_dict = dict(
            [
                map(lambda x: x.text.strip(), list_item.find_all(name="span"))
                for list_item in items
            ]
        )

        date_time = None
        date_range = None

        date_strs = self.date_pattern.findall(item_dict["기간"])
        if len(date_strs) == 1:
            date_str = date_strs[0]
            time_str = self.time_pattern.findall(item_dict["시간"])[0]
            date_time = datetime.strptime(
                f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        elif len(date_strs) == 2:
            date_range = list(map(
                lambda date_str: datetime.strptime(date_str, "%Y-%m-%d"), date_strs))
        else:
            raise ValueError("Invalid date format")

        location = self.location

        price_str = ""
        if "가격" in item_dict:
            raw_prices = self.price_pattern.findall(item_dict["가격"])
            comma_removed_prices = map(
                lambda raw: float(raw.replace(",", "")), raw_prices
            )
            prices = list(
                map(
                    lambda price: price / 10000 if price >= 1000 else price,
                    comma_removed_prices,
                )
            )

            if len(prices) > 0:
                min_price = min(prices)
                max_price = max(prices)
                price_str = f"{min_price}~{max_price}" if min_price != max_price else str(
                    min_price
                )

        print(f"Extracted {url}")

        return Program(
            title=title,
            date_time=date_time,
            date_range=date_range,
            location=location,
            url=url,
            price_str=price_str,
        )

    def get_programs_from_urls(self, urls: list[str]) -> list[Program]:
        return list(map(self.get_program_from_url, urls))
