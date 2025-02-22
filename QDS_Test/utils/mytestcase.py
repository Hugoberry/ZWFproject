# coding=utf-8
import unittest
import time

# from config.globalparam import driver_path
from utils.log import Log
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.pyselenium import logger


class MyTestCase(unittest.TestCase):
    """
    The base class is for all test cases. This is a father .
    """
    success = "SUCCESS   "
    fail = "FAIL   "
    logger = Log()

    def setUp(self):
        self.logger = Log()
        self.logger.info('############################### START ###############################')
        # chrome_options = Options()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument('--headless')
        # self.driver = webdriver.Chrome(options=chrome_options)
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(30)

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()
        self.logger.info('###############################  END  ###############################')

    @staticmethod
    def my_print(msg):
        logger.info(msg)
