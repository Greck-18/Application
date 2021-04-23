from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import lxml
import pprint as pp
from requests_html import HTMLSession
import re
from datetime import datetime


SELECTORS = {
    "title": (
        "body > div.top-container > div.wrapper-3-col >"
        " div > div > div.wrapper-3-col__center > h1"
    ),
    "date": (
        "body > div.top-container > div.wrapper-3-col >"
        " div > div > div.wrapper-3-col__center > div.news-article > div.news-article__details > p"
    ),
    "content": (
        "body > div.top-container > div.wrapper-3-col > div > div > div.wrapper-3-col__center > div.news-article > div.news-article__content"
    ),
}


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
        self._num_page = num_page
        self._links = []

    def check_num_page(self):
        try:
            pager = self.dom.find("div", class_="pager")
            active_page = pager.find("span", class_="pager__selected")
            return self._num_page == int(active_page.get_text())
        except Exception:
            return False

    def get_data(self):
        response = requests.get(self._url.format(self._num_page))
        if response.ok:
            self.dom = BeautifulSoup(response.text, "lxml")
        else:
            raise ValueError(f"Error {response.status_code}")

    def process_data(self):
        if not self.check_num_page():
            raise ValueError(f"Number of page {self._num_page} out of range")
        try:
            conteiner = self.dom.find("div", class_="wrapper-3-col__center")
        except AttributeError:
            raise AttributeError("Call method get_data()")
        conteiner = conteiner.find("div", class_="news__archive")
        links = conteiner.find_all("a", class_="news__story-title-link")
        self._links = [a["href"] for a in links]


    @property
    def links(self):
        return self._links

    def save_data(self):
        ...


class ParserNews(Parser):
    _pattern = re.compile(r"[rdthsn]+")
    _clean_pattern=re.compile(r"\n+")

    def __init__(self, url):
        self._url = url
        self._news = {}

    def get_data(self):

        session = HTMLSession()
        response = session.get(self._url)
        if response.status_code == 200:
            self.dom = response.html
        else:
            raise ValueError(f"Error! was returned {response.status_code}")

    def process_data(self):
        try:
            title = self.dom.find(SELECTORS["title"], first=True)
            date = self.dom.find(SELECTORS["date"], first=True)
            content = self.dom.find(SELECTORS["content"], first=True)
        except AttributeError:
            raise AttributeError("Call get_data()")

        d = date.text.split(" ")[1:]
        d[0] = self._pattern.sub("", d[0])
        self._news.update(
            title=title.text,
            date=datetime.strptime(" ".join(d), "%d %b %Y %H:%M"),
            content=self._clean_pattern.sub(" ",content.text),
            url=self._url
        )

    @property
    def news(self):
        return self._news

    def save_data(self):
        ...


if __name__ == "__main__":
    link_parser = ParserLinks(1)
    link_parser.get_data()
    link_parser.process_data()
