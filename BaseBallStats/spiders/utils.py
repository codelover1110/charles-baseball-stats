from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_spider(spider_name, url=None):
    settings = get_project_settings()

    # Update settings if a custom setting is provided
    process = CrawlerProcess(settings)
    process.crawl(spider_name, None,{'url': url})
    process.start()
    process.join()


def convert_to_mysql_date(date_string):
    # Define the input and output formats
    input_format = "%A, %B %d, %Y"
    output_format = "%Y-%m-%d"

    # Parse the input date string
    parsed_date = datetime.strptime(date_string, input_format)

    # Convert the parsed date to the desired output format
    mysql_date = parsed_date.strftime(output_format)

    return mysql_date


def convert_to_date_object(date_string, date_format = "%A, %B %d, %Y"):
    return datetime.strptime(date_string, date_format)

def convert_date_to_mysql_date(date_object):
    return date_object.strftime("%Y-%m-%d")

def convert_mysql_date_to_date(date_string):
    input_format = "%Y-%m-%d"
    return datetime.strptime(date_string, input_format)