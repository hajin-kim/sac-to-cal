from notion_client import Client

from Program import Program


class NotionApiClient(object):
    def __init__(self, auth: str, databaseId: str):
        self.client = Client(auth=auth)
        self.databaseId = databaseId

    def post_all(self, programs: list[Program]):
        for program in programs:
            self.post(program)

    def post(self, program: Program):
        parent = {"database_id": self.databaseId}
        properties = {
            "제목": {
                "title": [
                    {
                        "text": {
                            "content": program.title}}]},
            "일정": {
                "date": {
                    "start": program.date_time.strftime("%Y-%m-%dT%H:%M:%S+09:00")}},
            "장소": {
                "rich_text": [
                    {
                        "text": {
                            "content": program.location}}]},
            "URL": {
                "url": program.url},
            "예매/할인": {
                "rich_text": [
                    {
                        "text": {
                            "content": program.price_str}}]},
        }

        self.client.pages.create(
            parent=parent,
            properties=properties,
        )

        print(f"Posted {program.url}")
