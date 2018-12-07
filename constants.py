import os
import configparser
config = configparser.ConfigParser()
config.read("config.txt")

GOOG_ID = 'ishandutta2007'
GOOG_PASS = config.get("configuration", "goog_ishandutta2007_password")

LINKEDIN_ID = 'ishandutta2007@gmail.com'
LINKEDIN_PASS = config.get("configuration", "linkedin_ishandutta2007_password")

CHROME_DRIVER_PATH = '/Users/ishandutta2007/Documents/Projects/chromium/chromium/src/out/Default/chromedriver_gleam'

LINKEDIN_LOGIN_URL = 'https://www.linkedin.com/uas/login/'
LINKEDIN_SEARCH_URL = 'https://www.linkedin.com/search/results/people/?keywords='
