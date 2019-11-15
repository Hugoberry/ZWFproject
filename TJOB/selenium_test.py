import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()
driver.maximize_window()
driver.set_window_size(1920, 1080)

driver.get("https://www.zhipin.com/?city=101010100")
driver.execute_script("window.open('https://www.lagou.com/landing-page/pc/search.html?utm_source=m_cf_cpt_baidu_pcbt')")
windows = driver.window_handles
driver.switch_to.window(windows[0])
time.sleep(10)
driver.switch_to.window(windows[1])
pass
