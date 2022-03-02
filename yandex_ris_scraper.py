# this script deploys a reverse image search on google for a given source image and scrape search results
import csv
import time
import sys
from os import path
from selenium import webdriver
from bs4 import BeautifulSoup
from pathlib import Path
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import pandas as pd

# url of the source image (e.g. iconic image)
source_url = 'https://media.wired.com/photos/5dbafc6d8ebd000007e1447e/master/pass/Biz-Zuck-AP_19298678555254.jpg'

# selenium webdriver settings

# TODO: choose your local path to the downloaded webdriver
webdriver_path = '/Users/work/GitHub/plexxxi/webdriver/chromedriver'
# the options object can store settings for your zombie browser
options = Options()
# choose incognito mode to open a private window mode
options.add_argument("--incognito")
# for testing on your local computer with a GUI, have chrome installed and uncomment line below
options.add_argument("--headless")
# headless browsing works without GUI but needs fix window size for infinite scroll scraping
options.add_argument("window-size=1920,1080")

yandex_isearch = 'https://yandex.com/images/'