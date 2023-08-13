"""
Main entry point of this project
"""

import sys
from inputimeout import inputimeout, TimeoutOccurred
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from HtmlExtractor import HtmlExtractor
from CsvWriter import CsvWriter


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    html_extractor = providers.Singleton(HtmlExtractor)
    csv_writer = providers.Singleton(CsvWriter)


INPUT_TIMEOUT = 10  # in second


@inject
def main(
    argv: list[str],
    html_extractor: HtmlExtractor = Provide[Container.html_extractor],
    csv_writer: CsvWriter = Provide[Container.csv_writer],
) -> None:
    if len(argv) > 1:
        with open(argv[1], encoding="utf-8") as f:
            urls = [url.strip() for url in f.readlines() if len(url.strip()) > 0]
            programs = html_extractor.get_programs_from_urls(urls)
            csv_writer.write_csv_from_programs(programs)
    else:
        command = None
        try:
            command = str(inputimeout(prompt=">>", timeout=INPUT_TIMEOUT))
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
