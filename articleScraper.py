import newspaper
from newspaper import Article
import datetime
import requests
from bs4 import BeautifulSoup

class OpenArticle:
	authors = ""
	date = ""
	text = ""
	characterCount = ""
	wordCount = ""

def clean_url(originalAllSidesURL):
	if "www.allsides.com" not in originalAllSidesURL:
		return originalAllSidesURL

	all_sides_html = requests.get(originalAllSidesURL).text
	all_sides_soup = BeautifulSoup(all_sides_html, 'html.parser')

	hidden_link_div = all_sides_soup.find('div', class_='article-link-hidden')
	if hidden_link_div is None:
		return originalAllSidesURL

	return hidden_link_div.text.strip()

def scrape_article(listOfAllsideUrls):
	resultArticles = []

	for dirtyUrl in listOfAllsideUrls:
		url = clean_url(dirtyUrl)

		try:
			article = Article(url)
			article.download()
			#article.html

			article.parse()
			authors = article.authors
			date = article.publish_date
			text = article.text
			characterCount = len(text)
			wordCount = len(text.split())

			article = OpenArticle()

			if (len(authors) > 0):
				article.authors = ', '.join(authors)
			else:
				article.authors = None

			article.date = date
			article.text = text
			article.characterCount = characterCount
			article.wordCount = wordCount
			resultArticles.append(article)
		except:
			continue

	# print(len(resultArticles))
	# for article in resultArticles:
	# 	print(article.date)
	# 	print(article.authors)
	# 	print(article.characterCount)
	# 	#print(article.text)

	return resultArticles

#scrape_article(['https://www.allsides.com/news/2018-08-30-0726/biden-and-mccains-longtime-friendship-be-display-memorial-service'])
