import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.PhantomJS(executable_path="D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
driver.get("https://kns.cnki.net/kns/brief/default_result.aspx")

wait = WebDriverWait(driver, 60, 5)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#btnSearch')))
driver.find_element_by_css_selector(".research > .rekeyword").send_keys("物理")
driver.find_element_by_css_selector('#btnSearch').click()
time.sleep(5)
driver.refresh()
cookieJar = dict()
cookies = driver.get_cookies()
for cookie in cookies:
    cookieJar[cookie["name"]] = cookie["value"]
driver.close()
pass
