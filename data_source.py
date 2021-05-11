from abc import ABCMeta, abstractmethod, ABC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import chromedriver_binary


class DataSource(metaclass=ABCMeta):
    @abstractmethod
    def get_data_by_url(self, data_url: str) -> dict:
        pass


class Mora(DataSource):

    def __init__(self, chromedriver_path: str = None):
        super(Mora, self).__init__()
        options = webdriver.ChromeOptions()
        options.headless = True
        if chromedriver_path:
            options.binary_location = chromedriver_path
        self.driver = webdriver.Chrome(chrome_options=options)

    def get_data_by_url(self, data_url: str) -> list:
        self.driver.get(url=data_url)
        WebDriverWait(self.driver, 10)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        data = dict()

        data['album'] = soup.select("div#package_title")[0].text
        data['album_artist'] = soup.select("div#package_artist")[0].text
        data['release_date'] = soup.select("div#package_release")[0].text
        data['songs'] = dict();
        table_body = soup.select(".package_table")[0].findNext('tbody')
        for line in table_body.select("tr"):
            song = dict()
            for cell in line.select("td"):
                if "<!--No-->" in str(cell):
                    song['id'] = cell.text
                elif "<!--アーティスト名-->" in str(cell):
                    song['artist'] = cell.text
                if "<!--楽曲名-->" in str(cell):
                    song['name'] = cell.text
            data['songs'][song['id']] = song

        return data
