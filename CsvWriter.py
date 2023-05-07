from csv import DictWriter

from Program import Program


class CsvWriter(object):
    def __init__(self):
        self.field_header_dict = {
            'title': '제목',
            'date_time': '일정',
            'location': '장소',
            'undefined1': '일행',
            'url': 'URL',
            'undefined2': '예매/할인',
            'undefined3': '관심곡',
            'undefined4': '추천',
            'undefined5': '아티스트',
            'undefined6': '테마',
        }

    def write_csv_from_programs(self, programs: list[Program]) -> None:
        field_names = self.field_header_dict.keys()

        with open('./output.csv', 'w', encoding='utf-8') as f:
            writer = DictWriter(f, fieldnames=field_names)
            writer.writerow(self.field_header_dict)

            for program in programs:
                writer.writerow(program.__dict__)
