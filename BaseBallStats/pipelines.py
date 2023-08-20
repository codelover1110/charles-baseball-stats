# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlalchemy
from scrapy.exceptions import DropItem
from BaseBallStats.settings import DATABASE_CONNECTION_STRING, BUFFER_SIZE
from .items import PitchingItem, HittingItem, GameItem
from scrapy.crawler import CrawlerProcess
from .spiders.utils import run_spider
import scrapy
from scrapy.utils.defer import defer_result
from twisted.internet.defer import Deferred

from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import sessionmaker


class BaseballstatsPipeline:
    def __init__(self):
        self.engine = sqlalchemy.create_engine(DATABASE_CONNECTION_STRING)
        self.batch_size = BUFFER_SIZE  # Adjust as needed
        self.item_buffer = []
        self.tables = {}

    def get_table(self, table_name, column_names):
        if not table_name in self.tables:
            metadata = sqlalchemy.MetaData()

            columns = []
            for column_name in column_names:
                if column_name == 'GameDate':
                    column = sqlalchemy.Column(column_name, sqlalchemy.Date)
                else:
                    column = sqlalchemy.Column(column_name, sqlalchemy.String)
                columns.append(column)

            table = sqlalchemy.Table(table_name,
                metadata,
                sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                *columns
            )
            self.tables[table_name] = table
        return self.tables[table_name]

    def process_item(self, item, spider):
        try:
            self.item_buffer.append(item)
            if len(self.item_buffer) >= self.batch_size:
                self.insert_batch()
            return item
        except Exception as e:
            print('Exception:', e)
            raise DropItem(f"Failed to insert item into database: {e}")

    def insert_batch(self):
        print(f'==> inserting batch for {len(self.item_buffer)} records in buffer')
        Session = sessionmaker(bind=self.engine)
        session = Session()
        for item in self.item_buffer:
            item_data = item['row']
            table_name = 'pitching' if isinstance(item, PitchingItem) else 'hitting'
            table = self.get_table(table_name, item_data)
            ins = table.insert().values(item_data)
            session.execute(ins)
        session.commit()
        session.close()
        self.item_buffer = []

    def close_spider(self, spider):
        if self.item_buffer:
            self.insert_batch()
        # self.connection.close()

