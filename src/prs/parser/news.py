from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import lxml
import pprint as pp


class Parser(ABC):
    @abstractmethod
    def get_data(self):
        ...

    @abstractmethod
    def process_data(self):
        ...

    @abstractmethod
    def save_data(self):
        ...


class ParserLinks(Parser):
    _url = "https://www.lse.co.uk/news/archive.html?page={}"

    def __init__(self, num_page):
        self.num_page = num_page
        self._links=[]

    def get_data(self):
        response = requests.get(self._url.format(self.num_page))
        if response.ok:
            self.dom = BeautifulSoup(response.text, "lxml")
        else:
            raise ValueError(f"Error {response.status_code}")

    def process_data(self):
        try:
            conteiner = self.dom.find("div", class_="wrapper-3-col__center")
        except AttributeError:
            raise AttributeError("Call method get_data()")
        conteiner = conteiner.find("div", class_="news__archive")
        links = conteiner.find_all("a", class_="news__story-title-link")
        self._links=[a['href'] for a in links]
        pp.pprint(self._links)

    def save_data(self):
        ...


class ParserNews(Parser):
    def get_data(self):
        ...

    def process_data(self):
        ...

    def save_data(self):
        ...


if __name__ == "__main__":
    link_parser = ParserLinks(0)
    link_parser.get_data()
    link_parser.process_data()
