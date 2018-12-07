import os, datetime, time, sys, pickle
from random import randint
import re
import requests
import random
import argparse

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    UnexpectedAlertPresentException, WebDriverException
from pip._vendor.distlib.util import proceed
import constants
from more_itertools import unique_everseen

def login(driver):
	driver.get(constants.LINKEDIN_LOGIN_URL)
	username = driver.find_element_by_id("username")
	username.send_keys(constants.LINKEDIN_ID)
	username.send_keys(Keys.ENTER)
	password = driver.find_element_by_id("password")
	password.send_keys(constants.LINKEDIN_PASS)
	password.send_keys(Keys.ENTER)

def search_linkedin_profiles(driver):
	investor_profiles = []
	for search_term in ["Venture%20Capitalist", "Venture%20Capital", "Angel%20Investor", "Early%20Stage%20Investor"]:
		for pageno in range(1, 3):
			driver.get(constants.LINKEDIN_SEARCH_URL + search_term + "&page=" + str(pageno))
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
			links = driver.find_elements_by_css_selector("div.search-result__wrapper div.search-result__info a.search-result__result-link")
			for link in links:
				investor_profiles.append(link.get_attribute("href"))
				print(link.get_attribute("href"))
	return investor_profiles

def get_avoid_profiles(driver):
	return []

def fetch_and_save_email_list(driver, investor_profiles, avoid_profiles):
	with open('email-list.csv','a') as file:
		for investor_profile in investor_profiles:
			if investor_profile not in avoid_profiles:
				driver.get(investor_profile + 'detail/contact-info/')
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(3)

				name = driver.find_element_by_css_selector("h1").text

				links = driver.find_elements_by_css_selector("section a")
				for link in links:
					if  "@" in link.get_attribute("href"):
						line = link.get_attribute("href").replace('mailto:','') + ', ' + name + ', ' + investor_profile
						file.writelines(line)
						print(line)

def dedup():
	with open('email-list2.csv','w') as out_file:
		with open('email-list.csv','r') as f:		
			out_file.writelines(unique_everseen(f))

	os.rename('email-list.csv', 'email-list.csv.bkp')
	os.rename('email-list2.csv', 'email-list.csv')

if __name__ == '__main__':
	driver = webdriver.Chrome(constants.CHROME_DRIVER_PATH)
	login(driver)
	investor_profiles = search_linkedin_profiles(driver)
	avoid_profiles = get_avoid_profiles(driver)
	fetch_and_save_email_list(driver, investor_profiles, avoid_profiles)
	dedup()
	driver.quit()

