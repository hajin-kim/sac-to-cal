"""
Main entry point of this project
"""

import sys
import os
from inputimeout import inputimeout, TimeoutOccurred
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv

from SacHtmlExtractor import SacHtmlExtractor
from LotteHtmlExtractor import LotteHtmlExtractor
from CsvWriter import CsvWriter
from NotionApiClient import NotionApiClient
from Program import Program


load_dotenv()

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = os.environ.get("DATABASE_ID")
INPUT_TIMEOUT_SECONDS = int(os.environ.get("INPUT_TIMEOUT_SECONDS"))


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    sac_html_extractor = providers.Singleton(SacHtmlExtractor)
    lotte_html_extractor = providers.Singleton(LotteHtmlExtractor)
    csv_writer = providers.Singleton(CsvWriter)
    notion_api_client = providers.Singleton(
        NotionApiClient, auth=NOTION_API_KEY, databaseId=DATABASE_ID)


@inject
def main(
    argv: list[str],
    sac_html_extractor: SacHtmlExtractor = Provide[Container.sac_html_extractor],
    lotte_html_extractor: LotteHtmlExtractor = Provide[Container.lotte_html_extractor],
    csv_writer: CsvWriter = Provide[Container.csv_writer],
    notion_api_client: NotionApiClient = Provide[Container.notion_api_client],
) -> None:
    def process_url_to_program(url: str) -> Program:
        if 'lotteconcerthall' in url:
            return lotte_html_extractor.get_program_from_url(url)
        else:
            return sac_html_extractor.get_program_from_url(url)

    if len(argv) > 1:
        with open(argv[1], encoding="utf-8") as f:
            urls = [url.strip()
                    for url in f.readlines() if len(url.strip()) > 0]

            programs = [process_url_to_program(url) for url in urls]
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
            print(sac_html_extractor.get_programs_from_urls(command).__dict__)


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])

    main(sys.argv)
