import newspaper
from newspaper import Article
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import socket

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("headless")
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
driver = webdriver.Chrome(chrome_options=options)

def scrapeArticle(listOfAllsideUrls):
	articleDict = dict()
	for url2 in listOfAllsideUrls:
		try:
			driver.get(url2)
			python_button = driver.find_elements_by_class_name("open-new-page")

			python_button[0].click()
			url = driver.current_url
			article = Article(url)
			article.download()
			article.html

			article.parse()
			authors = article.authors
			date = article.publish_date
			text = article.text
			characterCount = len(text)
			wordCount = len(text.split())
			articleDict[url2]=(authors,date,text,characterCount,wordCount)
			print(articleDict[url2])
		except:
			continue

scrapeArticle(['https://www.allsides.com/news/2018-08-30-0726/biden-and-mccains-longtime-friendship-be-display-memorial-service'])

driver.close()