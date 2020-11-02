from models.enums.response_type import ResponseType
from models.proxy import Proxy

from utils.calculate import median

import datetime
import requests
import re

import traceback

import urllib3
urllib3.disable_warnings()

class Player:
    def __init__(self, name, id, position, version, rating):
        self.NAME = name
        self.ID = id
        self.POSITION = position
        self.VERSION = version
        self.RATING = rating

    def pull_sales(self, proxy, platform='pc'):
        try:
            req = requests.session()

            req.proxies = proxy.get_proxy()
            req.verify = False

            req.headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.284',
                'Accept':'application/json, text/javascript, */*; q=0.01',
                'Accept-Language':'en-US,en;q=0.9',
                'X-Requested-With':'XMLHttpRequest'
            }

            

            response = req.get(f'https://www.futbin.com/21/getPlayerSales?resourceId={self.ID}&platform={platform}')

            if response.status_code != 200:
                return ResponseType.BANNED
            if 'No Record Found' in response.text:
                self.STATS = {
                'LAST_SALES': 0,
                'HIGH':0,
                'HIGH_DAY':0,
                'LOW':0,
                'LOW_DAY':0,
                'DIFFERENCE': 0,
                'VOLUME':0,
                'AVERAGE': {
                    'ONE':0,
                    'FIVE':0,
                    'TEN':0
                },
                'MEDIAN': {
                    'ONE':0,
                    'FIVE':0,
                    'TEN':0
                }
            }
                return ResponseType.FAILURE
            response = response.json()


            closed_sale_prices = []
            closed_sales = []

            for sale in response:
                if sale['status'] == 'closed':
                    closed_sales.append(sale)
                    closed_sale_prices.append(sale['Price'])

            HIGH_PRICE = 0
            HIGH_DAY = ''

            for sale in closed_sales:
                if int(sale['Price']) > HIGH_PRICE:
                    HIGH_PRICE = int(sale['Price'])
                    HIGH_DAY = datetime.datetime.strptime(sale['updated'], '%Y-%m-%d %H:%M:%S').strftime('%A %b %d, %Y %H:%M')

            LOW_PRICE = 0
            LOW_DAY = ''

            for sale in closed_sales:
                if int(sale['Price']) < LOW_PRICE or LOW_PRICE == 0:
                    LOW_PRICE = int(sale['Price'])
                    LOW_DAY = datetime.datetime.strptime(sale['updated'], '%Y-%m-%d %H:%M:%S').strftime('%A %b %d, %Y %H:%M')

            one_day_sales = []
            five_day_sales = []
            ten_day_sales = []

            for sale in closed_sales:
                sale_date = datetime.datetime.strptime(sale['updated'], '%Y-%m-%d %H:%M:%S')
                if sale_date > datetime.datetime.utcnow()+datetime.timedelta(days=-1):
                    one_day_sales.append(sale['Price'])
                if sale_date > datetime.datetime.utcnow()+datetime.timedelta(days=-5):
                    five_day_sales.append(sale['Price'])
                if sale_date > datetime.datetime.utcnow()+datetime.timedelta(days=-10):
                    ten_day_sales.append(sale['Price'])

            VOLUME = len(one_day_sales)

            one_day_average = req.get(f'https://www.futbin.com/getPlayerAvgSell?days=1&resourceId={self.ID}&platform={platform}').json()['avg_sell_price']
            five_day_average = req.get(f'https://www.futbin.com/getPlayerAvgSell?days=5&resourceId={self.ID}&platform={platform}').json()['avg_sell_price']
            ten_day_average = req.get(f'https://www.futbin.com/getPlayerAvgSell?days=10&resourceId={self.ID}&platform={platform}').json()['avg_sell_price']

            one_day_median = median(one_day_sales)
            five_day_median = median(five_day_sales)
            ten_day_median = median(ten_day_sales)

            self.STATS = {
                'LAST_SALES': closed_sale_prices[:5],
                'HIGH':HIGH_PRICE,
                'HIGH_DAY':HIGH_DAY,
                'LOW':LOW_PRICE,
                'LOW_DAY':LOW_DAY,
                'DIFFERENCE': HIGH_PRICE-LOW_PRICE,
                'VOLUME':VOLUME,
                'AVERAGE': {
                    'ONE':one_day_average,
                    'FIVE':five_day_average,
                    'TEN':ten_day_average
                },
                'MEDIAN': {
                    'ONE':one_day_median,
                    'FIVE':five_day_median,
                    'TEN':ten_day_median
                }
            }

            return ResponseType.SUCCESS

        except:
            print(traceback.format_exc())
            return ResponseType.BANNED
    
    def __eq__(self, other):
        if other.NAME == self.NAME and other.RATING == self.RATING and other.POSITION == self.POSITION:
            return True

        return False