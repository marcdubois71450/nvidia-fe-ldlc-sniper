import logging
from selenium import webdriver
from logging.handlers import SysLogHandler
from selenium.webdriver.chrome.options import Options


from check import card_is_ok
from buy import buy_ldlc

from config import LDLC_ACCOUNT, CARD


link = ''



logger = logging.getLogger("nvidia-fe-ldlc-sniper-twetter")
logger.setLevel('DEBUG')
syslog = SysLogHandler('/dev/log', 'syslog')
syslog.setLevel('DEBUG')
format_str = "nvidia-fe-ldlc-sniper-twetter: {message}"
formatter = logging.Formatter(format_str, style="{")
syslog.setFormatter(formatter)
logger.addHandler(syslog)
logger.info("nvidia-fe-ldlc-sniper-twetter started")

# Start Chrome
logger.info("chrome start ...")
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)
logger.info("chrome started")



r = buy_ldlc(link, LDLC_ACCOUNT, CARD, logger, driver)

print(r)
