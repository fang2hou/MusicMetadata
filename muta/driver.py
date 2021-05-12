from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_binary


class Driver():

    def __init__(self, chromedriver_path: str = None):
        options = webdriver.ChromeOptions()
        options.headless = True
        if chromedriver_path:
            options.binary_location = chromedriver_path
        self.driver = webdriver.Chrome(chrome_options=options)

    def fetch(self, url) -> str:
        self.driver.get(url=url)
        WebDriverWait(self.driver, 10)
        return self.driver.page_source

    def quit(self):
        self.driver.close()
        self.driver.quit()