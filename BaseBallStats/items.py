# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from bs4 import BeautifulSoup


def get_string_or_empty(value):
    return "" if value is None else value.strip()

def make_data_row(row_selector, headers):
    data_row = {}
    for header, key in headers.items():
        data = row_selector.xpath('.//td[@data-stat="'+key+'"]/text()').get()
        data_row[header] = get_string_or_empty(data)

    # get player name
    html_string = row_selector.xpath('.//th[@data-stat="player"]').extract_first()
    soup = BeautifulSoup(html_string, 'html.parser')
    first_header = next(iter(headers))
    data_row[first_header] = get_string_or_empty(soup.get_text())

    return data_row

class HittingItem(scrapy.Item):
    row = scrapy.Field()

    @staticmethod
    def assign_data(row_selector):
        headers = {
            'Batting': 'player',
            'AB': 'AB',
            'R': 'R',
            'H': 'H',
            'RBI': 'RBI',
            'BB': 'BB',
            'SO': 'SO',
            'PA': 'PA',
            'BA': 'batting_avg',
            'OBP': 'onbase_perc',
            'SLG': 'slugging_perc',
            'OPS': 'onbase_plus_slugging',
            'Pit': 'pitches',
            'Str': 'strikes_total',
            'WPA': 'wpa_bat',
            'aLI': 'leverage_index_avg',
            'WPA+':'wpa_bat_pos',
            'WPA-':'wpa_bat_neg',
            'cWPA': 'cwpa_bat',
            'acLI': 'cli_avg',
            'RE24': 're24_bat',
            'PO': 'PO',
            'A': 'A',
            'Details': 'details',
        }
        return make_data_row(row_selector, headers)


class PitchingItem(scrapy.Item):
    row = scrapy.Field()

    @staticmethod
    def assign_data(row_selector):
        headers = {
            'Pitching': 'player',
            'IP': 'IP',
            'H': 'H',
            'R': 'R',
            'ER': 'ER',
            'BB': 'BB',
            'SO': 'SO',
            'HR': 'HR',
            'ERA': 'earned_run_avg',
            'BF': 'batters_faced',
            'Pit': 'pitches',
            'Str': 'strikes_total',
            'Ctct': 'strikes_contact',
            'StS': 'strikes_swinging',
            'StL': 'strikes_looking',
            'GB': 'inplay_gb_total',
            'FB': 'inplay_fb_total',
            'LD': 'inplay_ld',
            'Unk': 'inplay_unk',
            'GSc': 'game_score',
            'IR': 'inherited_runners',
            'IS': 'inherited_score',
            'WPA': 'wpa_def',
            'aLI': 'leverage_index_avg',
            'cWPA': 'cwpa_def',
            'acLI': 'cli_avg',
            'RE24': 're24_def',
        }

        return make_data_row(row_selector, headers)


class GameItem(scrapy.Item):
    row = scrapy.Field()