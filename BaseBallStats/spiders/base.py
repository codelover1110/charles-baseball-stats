import scrapy
from BaseBallStats.items import GameItem, PitchingItem, HittingItem
from scrapy.utils.project import get_project_settings
import random
import selenium
from selenium.webdriver import Firefox,Chrome
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from scrapy.http import HtmlResponse
from BaseBallStats.settings import GECKODRIVER_PATH, CHROMEDRIVER_PATH

from datetime import datetime
from .utils import convert_to_mysql_date

import sqlalchemy
from BaseBallStats.settings import IS_WINDOWS_OS, DATABASE_CONNECTION_STRING
from sqlalchemy import create_engine, select, func, text
from sqlalchemy.orm import sessionmaker

class BaseSpider(scrapy.Spider):
    name = 'base_spider'
    allowed_domains = ['baseball-reference.com']
    must_remote = True

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.engine = sqlalchemy.create_engine(DATABASE_CONNECTION_STRING)
        if self.must_remote:
            self.setup_browser()

    def setup_browser(self):
        if IS_WINDOWS_OS:
            self.browser = self.create_firefox_browser()
        else:
            self.browser = self.create_chrome_browser()

    def create_chrome_browser(self):
        proxy_list = self.load_proxy_list()
        random_proxy_ip = random.choice(proxy_list)

        chrome_options = ChromeOptions()
        chrome_options.add_argument(f"--proxy-server={random_proxy_ip}")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors.
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')

        service = ChromeService(executable_path=CHROMEDRIVER_PATH)
        self.proxy_ip = random_proxy_ip
        return webdriver.Chrome(service=service, options=chrome_options)


    def create_firefox_browser(self):
        proxy_list = self.load_proxy_list()
        random_proxy_ip = random.choice(proxy_list)
        driver_path = GECKODRIVER_PATH
        service = Service(driver_path)

        DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": random_proxy_ip,
            "ftpProxy": random_proxy_ip,
            "sslProxy": random_proxy_ip,
            "proxyType": "MANUAL",
        }
        firefox_options = FirefoxOptions()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors.
        firefox_options.add_argument('--disable-dev-shm-usage')
        firefox_options.add_argument('--disable-gpu')
        self.proxy_ip = random_proxy_ip
        return webdriver.Firefox(service=service, options=firefox_options)

    def load_proxy_list(self):
        settings=get_project_settings()
        proxy_list = []
        proxy_filepath = settings.get('PROXY_LIST')
        with open(proxy_filepath) as f:
            tmp_list = f.readlines()
            for proxy in tmp_list:
                proxy_list.append(proxy.replace("\n",""))
        return proxy_list

    def get_response(self, response_url):
        if self.must_remote:
            response = self.get_remote_response(response_url)
        else:
            response = self.get_local_response(response_url)
        return response

    def get_remote_response(self, original_url):
        self.browser.get(original_url)
        # time.sleep(1) #sleep for 1 sec
        html_content = self.browser.page_source

        response = HtmlResponse(url=original_url, body=html_content, encoding='utf-8')
        return response

    def get_local_response(self, original_url):
        file_path = "{name}_content.txt".format(name=self.name)
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        response = HtmlResponse(url=original_url, body=html_content, encoding='utf-8')
        return response

    def closed(self, reason):
        if self.must_remote:
            self.browser.quit()