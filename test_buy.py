import logging
from selenium import webdriver
from logging.handlers import SysLogHandler
from selenium.webdriver.chrome.options import Options

from check import card_is_ok
from buy import buy_ldlc

from config import LDLC_ACCOUNT, CARD

link = 'https://www.ldlc.com/fiche/PB00102565.html'

logger = logging.getLogger("nvidia-fe-ldlc-sniper-test")
logger.setLevel('DEBUG')
syslog = SysLogHandler('/dev/log', 'syslog')
syslog.setLevel('DEBUG')
format_str = "nvidia-fe-ldlc-sniper-test: {message}"
formatter = logging.Formatter(format_str, style="{")
syslog.setFormatter(formatter)
logger.addHandler(syslog)
logger.info("nvidia-fe-ldlc-sniper-test started")

r = buy_ldlc(link, LDLC_ACCOUNT, CARD, logger)

print(r)
