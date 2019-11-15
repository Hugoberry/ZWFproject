import json
import random
import time

import redis
import requests
from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from main import num
# num = "0"
ip_cookie_key = 'ip_cookie_key_%s' % num
ua_ls = open("./my_tools/ua.txt", mode="r+", encoding="utf-8").readlines()
# ua_ls = open("./ua.txt", mode="r+", encoding="utf-8").readlines()


class IPCookie(object):

    def __init__(self):
        # self.redis_connect_pool = redis.ConnectionPool(host='40.73.36.3', port=6667, db=15, password='quandashi2018')
        self.redis_connect_pool = redis.ConnectionPool(host='10.0.7.6', port=6667, db=15, password='quandashi2018')
        self.connect = redis.StrictRedis(connection_pool=self.redis_connect_pool, decode_responses=True)

    @staticmethod
    def ip_for_selenium():

        text = requests.get('http://39.107.59.59/random').text
        json_text = json.loads(text)
        host = json_text['RESULT'][0]['ip']
        port = json_text['RESULT'][0]['port']

        return 'http://' + host + ':' + port

    def get_cookies(self):

        ip = self.ip_for_selenium()
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--proxy-server=%s" % ip)
        ua = random.choice(ua_ls).replace("\n", "")
        chrome_options.add_argument('user-agent=%s' % ua)
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.set_window_size(1920, 1080)
        # url = 'https://euipo.europa.eu/eSearch/#details/trademarks/000000001'
        url = 'https://euipo.europa.eu/eSearch/'
        try:
            driver.get(url)
            time.sleep(20)
            if driver.title == "EUIPO - eSearch":
            # wait = WebDriverWait(driver, 60, 5)
            # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login-info')))
                cookies = driver.get_cookies()
                cookie_jar = {}
                for cookie in cookies:
                    name = cookie['name']
                    value = cookie['value']
                    cookie_jar[str(name)] = str(value)

                str_cookie = json.dumps(dict(cookie_jar), ensure_ascii=False)
                cookie_ip_ls = [ip, str_cookie]
                print(cookie_ip_ls)
                driver.close()
                return self.connect.lpush(ip_cookie_key, str(cookie_ip_ls))
            else:
                raise Exception
        except Exception as e:
            driver.close()
            print(e)
            self.get_cookies()


get_cookie = IPCookie().get_cookies()
