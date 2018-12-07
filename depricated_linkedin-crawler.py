import os, sys, unittest, time, re, requests
from bs4 import BeautifulSoup
import traceback

import json
import hashlib
import urllib.error
from urllib.request import Request, urlopen, build_opener, install_opener, HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
from lxml import etree
import csv
import time
import logging
from datetime import date, timedelta
import subprocess
from requests import session

import argparse
import constants
import pprint
pp = pprint.PrettyPrinter(indent=4)

USER = constants.LINKEDIN_ID
PASSWORD = constants.LINKEDIN_PASS
# LINKEDIN_LOGIN_URL = 'https://www.linkedin.com/m/login/'
LINKEDIN_LOGIN_URL = 'https://www.linkedin.com/uas/login/'#?formSignIn=true&session_redirect=%2Fvoyager%2FloginRedirect.html&one_time_redirect=https%3A%2F%2Fwww.linkedin.com%2Fm%2Flogin%2F'
LINKEDIN_SUBMIT_URL = 'https://www.linkedin.com/checkpoint/lg/login-submit'

def get_bio(s, fork_url):
	profile_url = '/'.join(fork_url.split('/')[0:-1])
	html_source = s.get(profile_url).text
	line = ''
	try:
		parsed_html = BeautifulSoup(html_source, 'html.parser')

		username_val = profile_url.split('/')[-1]
		print('username:', username_val)
		line = line + username_val + ', '

		print('repourl:', fork_url)
		line = line + fork_url + ', '

		fullname = parsed_html.find("span", class_="vcard-fullname")
		if fullname is not None:
			fullname_val = fullname.find(text=True, recursive=False)
			print('fullname:', fullname_val)
			if fullname_val is not None:
				line = line + fullname_val
		line = line + ', '

		email_li = parsed_html.find("li", {'itemprop':"email"}, class_="vcard-detail")
		if email_li is not None:
			email = email_li.find("a", class_="u-email")
			if email is not None:
				email_val = email.find(text=True, recursive=False)
				print('email: ', email_val)
				if email_val is not None:
					line = line + email_val
		line = line + ', '

		org_li = parsed_html.find("li", {'itemprop':"worksFor"}, class_="vcard-detail")
		if org_li is not None:
			org = org_li.find("span", class_="p-org")
			if org is not None:
				org_val = org.find(text=True, recursive=True)
				print('organisation:', org_val)
				if org_val is not None:
					line = line + org_val

		line = line + '\n'
		print()
	except Exception:
		traceback.print_exc()
	return line

def get_investors_url(root_url):
	profile_urls = []
	try:
		req = Request(root_url , headers={'User-Agent': 'Mozilla/5.0'})
		html_source = urlopen(req).read()
		parsed_html = BeautifulSoup(html_source, 'html.parser')
		# pp.pprint(parsed_html)
		links = parsed_html.find_all("a")#, class_="repo")

		for l in links:
			print(l['href'])
			# if len(l['href'].split('/')) > 2:
				# profile_urls.append("https://github.com" + l['href'])

		# print(a_)
		
		# for fork in forks:
		# 	links = fork.find_all("a", class_="")
		# 	prinr(links)
		# 	profile_urls.append(links)
			# for l in links:
			# 	if len(l['href'].split('/')) > 2:
			# 		profile_urls.append("https://github.com" + l['href'])
	except urllib.error.URLError as e:
		print("Seems URL changed for: " + root_url)
		print(e)
	except Exception as e:
		print("Unknown Error: " + root_url)
		print(e)
	return profile_urls

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--repo', default="https://www.linkedin.com/search/results/people/?keywords=Venture%20Capitalist")
	args = parser.parse_args()
	with session() as s:
		req = s.get(LINKEDIN_LOGIN_URL).text
		html = BeautifulSoup(req, 'html.parser')

		csrfToken = html.find("input", {"name": "csrfToken"}).attrs['value']
		ac = html.find("input", {"name": "ac"}).attrs['value']
		sIdString = html.find("input", {"name": "sIdString"}).attrs['value']
		controlId = html.find("input", {"name": "controlId"}).attrs['value']
		parentPageKey = html.find("input", {"name": "parentPageKey"}).attrs['value']
		pageInstance = html.find("input", {"name": "pageInstance"}).attrs['value']
		session_redirect = html.find("input", {"name": "session_redirect"}).attrs['value']
		# isJsEnabled = html.find("input", {"name": "isJsEnabled"}).attrs['value']
		loginCsrfParam = html.find("input", {"name": "loginCsrfParam"}).attrs['value']
		_d = html.find("input", {"name": "_d"}).attrs['value']

		login_data = {
			'csrfToken': csrfToken,
			'session_key': USER,
			'ac': ac,
			'sIdString': sIdString,
			'controlId': controlId,
			'parentPageKey': parentPageKey,
			'pageInstance': pageInstance,
			'trk': '',
			'session_redirect': session_redirect,
			'loginCsrfParam': loginCsrfParam,
			'_d': _d,
			'session_password': PASSWORD
		}


		resp = s.post(LINKEDIN_SUBMIT_URL, data = login_data)
		print(resp.url)

		resp2 = s.get(args.repo)
		print(resp2.url)
		req2html = resp2.text
		parsed_html = BeautifulSoup(req2html, 'html.parser')

		# pp.pprint(parsed_html)
		links = parsed_html.find_all("li")#, class_="repo")

		for l in links:
			print(l)#['href'])

		# profile_urls = get_investors_url(args.repo)
		# print(profile_urls)

	# with open('email-list.csv','wb') as file:
	# 	file.write(bytes('Username, RepoUrl, Fullname, EmailAddress, Organisation\n', 'UTF-8'))
	# 	with session() as s:
	# 		req = s.get(LINKEDIN_SESSION_URL).text
	# 		html = BeautifulSoup(req, 'html.parser')
	# 		token = html.find("input", {"name": "authenticity_token"}).attrs['value']
	# 		com_val = html.find("input", {"name": "commit"}).attrs['value']

	# 		login_data = {'login': USER,
	# 					'password': PASSWORD,
	# 					'commit' : com_val,
	# 					'authenticity_token' : token}

	# 		s.post(LINKEDIN_SESSION_URL, data = login_data)

	# 		for fork_url in profile_urls:
	# 			line = get_bio(s, fork_url)
	# 			file.write(bytes(line, 'UTF-8'))

if __name__ == '__main__':
  main()