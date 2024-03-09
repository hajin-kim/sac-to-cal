"""
Main entry point of this project
"""

import sys
import os
from inputimeout import inputimeout, TimeoutOccurred
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv

from HtmlExtractor import HtmlExtractor
from CsvWriter import CsvWriter
from NotionApiClient import NotionApiClient


load_dotenv()

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = os.environ.get("DATABASE_ID")
INPUT_TIMEOUT_SECONDS = int(os.environ.get("INPUT_TIMEOUT_SECONDS"))


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    html_extractor = providers.Singleton(HtmlExtractor)
    csv_writer = providers.Singleton(CsvWriter)
    notion_api_client = providers.Singleton(
        NotionApiClient, auth=NOTION_API_KEY, databaseId=DATABASE_ID)


@inject
def main(
    argv: list[str],
    html_extractor: HtmlExtractor = Provide[Container.html_extractor],
    csv_writer: CsvWriter = Provide[Container.csv_writer],
    notion_api_client: NotionApiClient = Provide[Container.notion_api_client],
) -> None:
    if len(argv) > 1:
        with open(argv[1], encoding="utf-8") as f:
            urls = [url.strip()
                    for url in f.readlines() if len(url.strip()) > 0]
            programs = html_extractor.get_programs_from_urls(urls)
            csv_writer.write_csv_from_programs(programs)
            notion_api_client.post_all(programs)
    else:
        command = None
        try:
            command = str(inputimeout(
                prompt=">>", timeout=INPUT_TIMEOUT_SECONDS))
        except TimeoutOccurred:
            print("Timeout occured.")

        if command is None:
            pass
        else:
            print(html_extractor.get_programs_from_urls(command).__dict__)


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    main(sys.argv)
