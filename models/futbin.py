from models.enums.response_type import ResponseType
from models.player import Player
from models.proxy import Proxy

import requests
import re

import urllib3
urllib3.disable_warnings()

class Futbin:
    def __init__(self, email, password):
        self.EMAIL = email
        self.PASSWORD = password
        self.session = None

    def login(self, proxy):
        try:
            SUCCESS_KEYS = ['{"success":true']
            FAILURE_KEYS = ['{"success":false']

            req = requests.session()

            req.proxies = proxy.get_proxy()
            req.verify = False

            req.headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.284',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language':'en-US,en;q=0.9',
                'Accept-Encoding':'gzip, deflate, br',
                'Referer':'https://www.futbin.com/'
            }

            response = req.get('https://www.futbin.com/account/login')

            if response.status_code != 200:
                return ResponseType.BANNED
            response = response.text

            self.csrf_name = re.search(r'<input class="login-csrf-name" value="(.*?)"', response)
            self.csrf_value = re.search(r'<input class="login-csrf-value" value="(.*?)"', response)

            self.gen_csrf_name = re.search(r'general_csrf-name\' content=\'(.*?)\'', response)
            self.gen_csrf_value = re.search(r'general_csrf-value\' content=\'(.*?)\'', response)

            if None in [self.csrf_name, self.csrf_value]:
                return ResponseType.BANNED
            self.csrf_name = self.csrf_name.group(1)
            self.csrf_value = self.csrf_value.group(1)
            self.gen_csrf_name = self.gen_csrf_name.group(1)
            self.gen_csrf_value = self.gen_csrf_value.group(1)

            req.headers['Accept'] = '*/*'
            req.headers['X-Requested-With'] = 'XMLHttpRequest'
            req.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            req.headers['Referer'] = 'https://www.futbin.com/account/login'

            response = req.post('https://www.futbin.com/auth/login', f'name={self.EMAIL}&password={self.PASSWORD}&forum=false&forum_target=&remember=true&csrf_name={self.csrf_name}&csrf_value={self.csrf_value}')
            
            if response.status_code != 200:
                return ResponseType.BANNED
            response = response.text

            if any(key in response for key in FAILURE_KEYS):
                return ResponseType.FAILURE
            elif any(key in response for key in SUCCESS_KEYS):
                self.session = req
                return ResponseType.SUCCESS

            return ResponseType.BANNED

        except:
            return ResponseType.BANNED

    def pull_favorites(self):
        if self.session is None:
            return []

        try:
            req = self.session

            req.get('https://www.futbin.com/tracker')

            req.headers['Referer'] = 'https://www.futbin.com/tracker'
            req.headers['Origin'] = 'https://www.futbin.com'
            req.headers['Sec-Fetch-Site'] = 'same-origin'
            req.headers['Sec-Fetch-Mode'] = 'cors'
            req.headers['Sec-Fetch-Dest'] = 'empty'

            response = req.post('https://www.futbin.com/user/auth/tracker/getFavPlayersP', f'csrf_name={self.gen_csrf_name}&csrf_value={self.gen_csrf_value}')

            if response.status_code != 200:
                return ResponseType.BANNED
            response = response.json()

            players = response['players']

            player_list = []

            for player in players:
                player_list.append(Player(player['name'], player['baseid'], player['position'], player['version'], player['rating']))

            return player_list

        except:
            return ResponseType.BANNED

    