import scrapy
from BaseBallStats.items import GameItem, PitchingItem, HittingItem
import random
import selenium
from selenium.webdriver import Firefox,Chrome
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from scrapy.http import HtmlResponse

from datetime import datetime, timedelta
from .utils import convert_to_mysql_date, convert_to_date_object, convert_date_to_mysql_date, convert_mysql_date_to_date

import sqlalchemy
from BaseBallStats.settings import DATABASE_CONNECTION_STRING
from sqlalchemy import create_engine, select, func, text
from sqlalchemy.orm import sessionmaker

from .base import BaseSpider

class SportSpider(BaseSpider):
    name = 'sport_scraper'

    def __init__(self, url=None, *args, **kwargs):
        print('Starting...')
        super(SportSpider, self).__init__(*args, **kwargs)
        (start_date, end_date) = self.get_date_range()
        last_date = self.get_the_last_date()
        if last_date != 'None' and last_date >= start_date:
            start_date = last_date + timedelta(days=1)
            print('The last date from DB:', convert_date_to_mysql_date(last_date))

        self.date_range = (start_date, end_date)
        print(f'Scraping game stores from {convert_date_to_mysql_date(start_date)} to {convert_date_to_mysql_date(end_date)}')

    def get_date_range(self):
        # return (convert_mysql_date_to_date('2023-03-30'), convert_mysql_date_to_date('2023-03-31'))

        schedule_url = 'https://www.baseball-reference.com/leagues/MLB-schedule.shtml'
        response = self.get_response(schedule_url)
        start_date = response.xpath('//div[@class="section_content"]/div/h3/text()').get()
        start_date = convert_to_date_object(start_date)
        end_date = response.xpath('//span[@id="today"]//parent::h3//parent::div//preceding::div[1]/h3/text()').get()
        end_date = convert_to_date_object(end_date)

        return (start_date, end_date)

    def get_the_last_date(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        raw_sql_query = """
            SELECT MAX(GameDate) as latest_date
            FROM hitting
        """
        result = session.execute(text(raw_sql_query)).fetchone()
        if result and result[0]:
            latest_date = convert_mysql_date_to_date(str(result[0]))
        else:
            latest_date = 'None'
        session.close()

        return latest_date

    def get_boxes_url(self, mysql_date):
        url = f'https://www.baseball-reference.com/boxes/?date={mysql_date}'
        return url

    def start_requests(self):
        (current_date, end_date) = self.date_range
        while current_date <= end_date:
            sql_date = convert_date_to_mysql_date(current_date)
            boxes_url = self.get_boxes_url(sql_date)
            game_urls = self.get_list_game_urls(boxes_url)
            for game_url in game_urls:
                game_full_url = f'https://www.baseball-reference.com{game_url}'
                yield scrapy.Request(game_full_url, callback=self.parse, meta={'current_date': sql_date, 'game_url': game_url})
            current_date += timedelta(days=1)

    def get_list_game_urls(self, boxes_url):
        response = self.get_response(boxes_url)
        game_summaries_list = response.xpath('//div[@id="content"]//div[@class="game_summaries"]')
        game_urls = []
        if len(game_summaries_list) > 0:
            game_summaries = game_summaries_list[0]
            game_urls = game_summaries.xpath('.//div[contains(@class, "game_summary")]//td[contains(@class, "gamelink")]/a/@href').getall()

        return game_urls

    def parse(self, response):
        try:
            print(response.meta['current_date'], response.meta['game_url'])
            response = self.get_response(response.url)

            # game data for all tables
            global_columns = {}
            global_columns['GameDate'] = convert_to_mysql_date(response.xpath('//div[@class="scorebox_meta"]/div/text()').get())
            global_columns['Date'] = response.xpath('//div[@class="scorebox_meta"]/div/text()').get()
            global_columns['HomeTeam'] = response.xpath('//div[@class="scorebox"]/div/div/strong/a/text()').get()
            global_columns['AwayTeam'] = response.xpath('//div[@class="scorebox"]/div[position()=2]/div/strong/a/text()').get()
            global_columns['HomeScore'] = response.xpath('//div[@class="scorebox"]/div/div[@class="scores"]/div/text()').get()
            global_columns['AwayScore'] = response.xpath('//div[@class="scorebox"]/div[position()=2]/div[@class="scores"]/div/text()').get()
            global_columns['GameURL'] = response.url


            # data on each table
            stats_tables = response.xpath('//table[contains(@class, "stats_table")]')
            for _, table in enumerate(stats_tables):
                first_cell_header = table.xpath('./thead/tr/th/text()').get()
                if first_cell_header != 'Batting' and first_cell_header != 'Pitching':
                    continue

                rows = table.xpath('./tbody/tr')
                for _, row in enumerate(rows):
                    row_class = row.xpath('./@class').get()
                    if row_class == 'spacer':
                        break

                    if first_cell_header == 'Batting':
                        item = HittingItem()
                        item['row'] = HittingItem.assign_data(row)
                    else:
                        item = PitchingItem()
                        item['row'] = PitchingItem.assign_data(row)

                    item['row'] = {**global_columns, **item['row']}
                    yield item
        except Exception as ex:
            self.log_error(response.meta['game_url'])

    def log_error(self, game_url):
        item_data = {
            'ip': self.proxy_ip,
            'game_url': game_url
        }
        engine = sqlalchemy.create_engine(DATABASE_CONNECTION_STRING)
        Session = sessionmaker(engine)
        session = Session()
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table('blocking_ips_game',
            metadata,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column('ip', sqlalchemy.String),
            sqlalchemy.Column('game_url', sqlalchemy.String),
        )

        ins = table.insert().values(item_data)
        session.execute(ins)
        session.commit()
        session.close()

        self.proxy_ip

    def closed(self, reason):
        print('DONE!')