import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import socket
import requests
import urllib2
import justext
import string
#driver = webdriver.Firefox()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("headless")
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
options.add_argument("user-agent=Chrome")
driver = webdriver.Chrome(chrome_options=options)

def printable(line):
	if (line == None):
		return ''
	filtered_string = filter(lambda x: x in string.printable, line)
	line = "".join(filtered_string)
	return line

def scrapeArticle(listOfAllsideUrls):
	articleDict = dict()
	for url2 in listOfAllsideUrls:
		date = None
		try:
			date = url2.split('/')[4].split('-')
			date = (date[1]+'/'+date[2]+'/'+date[0]).encode('ascii','ignore')
		except:
			pass
		l = list()
		try:
			driver.get(url2)
			python_button = driver.find_elements_by_class_name("open-new-page")
			python_button[0].click()
			url = driver.current_url
			response = requests.get(url)
			paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
			author = ""
			for paragraph in paragraphs:
				t = paragraph.text.encode('ascii','ignore').lower()
				if (not (paragraph.is_boilerplate) and (len(paragraph.text)>30)):
					l.append(printable(paragraph.text.encode('ascii','ignore')))
					if('...'in paragraph.text):
						break
				elif((len(t)<40) and (('by' in t) or ('author' in t))):
					author = t
			Article = '\n'.join(l)
			charCount = len(Article)
			wordCount = len(Article.split())
			articleDict[url2] = (Article,date,wordCount,charCount,author)
		except:
			continue
	return articleDict