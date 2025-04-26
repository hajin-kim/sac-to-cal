from bs4 import BeautifulSoup
from urllib import request
from datetime import datetime
import re

from Program import Program


class LotteHtmlExtractor(object):
    def __init__(self):
        self.date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
        self.time_pattern = re.compile(r"\d{2}:\d{2}")
        self.price_pattern = re.compile(r"(\d+만원)|(\d+천원)|(\d+만\d+천원)")
        self.location = "롯데콘서트홀"

    def download_html_to_soup(self, url: str) -> BeautifulSoup:
        with request.urlopen(url) as f:
            return BeautifulSoup(f.read(), "html5lib")

    def to_stripped_text(self, element) -> str:
        return "\n".join(filter(lambda x: x != "", element.stripped_strings))

    def get_program_from_url(self, url: str) -> Program:
        soup = self.download_html_to_soup(url)

        top_view = soup.find(attrs={"class": "f_con clfix"})

        title_texts = list(filter(lambda x: x != "", map(
            lambda x: x.text.strip(), top_view.find(attrs={"class": "title"}).children)))
        title = ": ".join(
            title_texts
        )

        items = top_view.find_all(attrs={"class": "show_guide clfix"})
        children_list = [
            list(filter(lambda x: x != "", map(
                self.to_stripped_text, list_item.children)))
            for list_item in items
        ]
        item_pairs = filter(
            lambda x: len(x) == 2,
            children_list,
        )
        item_dict = dict(item_pairs)

        date_time = None
        date_range = None

        date_strs = self.date_pattern.findall(item_dict["일자"])
        if len(date_strs) == 1:
            date_str = date_strs[0]
            time_str = self.time_pattern.findall(item_dict["공연시간"])[0]
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

            prices = []
            for raw_price in raw_prices:
                raw_price = "".join(raw_price)
                if "천" in raw_price:
                    raw_price = raw_price.replace("천원", "000")
                    raw_price = raw_price.replace("만", "")
                elif "만" in raw_price:
                    raw_price = raw_price.replace("만원", "0000")
                int_price = int(raw_price)
                price = int_price / 10000 if int_price >= 1000 else int_price
                prices.append(price)

            if len(prices) > 0:
                min_price = min(prices)
                max_price = max(prices)
                price_str = f"{min_price}~{max_price}" if min_price != max_price else str(
                    min_price
                )

        print(f"Extracted {url} by LotteHtmlExtractor")

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
