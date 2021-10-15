from dataclasses import dataclass


@dataclass
class Command:

    anri: object
    name: str

    def do_work(self, *args) -> None:
        print("Send A Command")


@dataclass
class Query:

    anri: object
    name: str

    def do_work(self, *args) -> None:
        print("Query done")


@dataclass
class Connector:

    anri: object
    name: str

    def do_work(self, *args) -> None:
        print("Connected to")