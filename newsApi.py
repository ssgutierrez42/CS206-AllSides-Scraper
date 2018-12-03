from newsapi.newsapi_client import NewsApiClient

import string
from newspaper import Article
import newspaper
from pprint import pprint
import scholarly
from googlesearch import search
from bs4 import BeautifulSoup
import requests
import urllib
from random import choice
from urllib.request import urlopen as uReq
import requests
from urllib.request import Request
import re
import search_google.api
import enum
from gsearch.googlesearch import search

#results = search('muckrack erik wemple')
#link = results[0][1]
buildargs = {
  'serviceName': 'customsearch',
  'version': 'v1',
  'developerKey': 'AIzaSyCdMqTmsONtYV8x4IHruTgIOQxzMAZRuBE'
}

def getAuthUrl(author):
    cseargs = {'q': author,'cx': '002127797185034144380:9cz4vhqwpfq','num': 1}
    results = search_google.api.results(buildargs, cseargs)
    return results.links[0]

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
 
def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

def printable(line):
	if (line == None):
		return ''
	filtered_string = filter(lambda x: x in string.printable, line)
	line = "".join(filtered_string)
	return line

#bigNewsList
bigNewsList = list()
bigNewsList.append('associated-press')
bigNewsList.append('cnn')
bigNewsList.append('google-news')
bigNewsList.append('the-washington-post')
bigNewsList.append('fox-news')
bigNewsList.append('the-guardian-uk')
bigNewsList.append('the-guardian-au')
bigNewsList.append('the-new-york-times')
bigNewsList.append('wired')
bigNewsList.append('bbc-news')
bigNewsList.append('al-jazeera-english')
bigNewsList.append('techcrunch')
bigNewsList.append('bloomberg')
bigNewsList.append('the-wall-street-journal')
bigNewsList.append('politico')
bigNewsList.append('espn')
bigNewsList.append('the-washington-times')
bigNewsList.append('bbc-sport')
bigNewsList.append('buzzfeed')
bigNewsList.append('the-huffington-post')
bigNewsList.append('usa-today')
bigNewsList.append('the-economist')
bigNewsList.append('the-times-of-india')
bigNewsList.append('xinhua-net')
bigNewsList.append('spiegel-online')
bigNewsList.append('reuters')
bigNewsList.append('entertainment-weekly')
bigNewsList.append('the-telegraph')
bigNewsList.append('le-monde')
bigNewsList.append('rt')
bigNewsList.append('the-hill')
bigNewsList.append('vice-news')

bigNews = ",".join(bigNewsList)

smallNews='bbc-news,fox-news,the-new-york-times,the-washington-post,the-wall-street-journal'
newsapi = NewsApiClient(api_key='e388bce4290446afa545681fac60366f')

class AuthorInformation:
    name = ""
    location = ""
    title = ""
    beats = ""
    description = ""


class NewsApiArticle:
    source = ""
    author = ""
    title = ""
    description = ""
    url = ""
    published = ""
    content = ""
    wordCount = 0
    topics = ""

def scrapeAuthorInfo(url):
    author = AuthorInformation()
    req = Request(url,headers=random_headers())
    page = uReq(req)
    soup = BeautifulSoup(page, 'lxml')
    try:
        author.description = soup.find("div", {"class": "profile-section profile-bio"}).text.strip()
    except:
        pass
    try:
        author.name = soup.find("h1", {"class": "profile-name mr-font-family-2 top-none"}).text.strip()
    except:
        pass
    try: 
        author.title = soup.find("div", {"class": "person-details-item person-details-title"}).text.strip().replace('\n', ' ')
        author.title = re.sub(' +',' ',author.title).encode('ascii',errors='ignore').decode("ascii")
        author.title = re.sub('  +',' for ',author.title)
    except:
        pass
    try:
        author.beats = soup.find("div", {"class": "person-details-item person-details-beats"}).text.strip().replace('\n','')
        author.beats = re.sub(' +',' ',author.beats).replace(', ',',')
    except:
        pass
    return author
 
def newsapi_scrape():
    print("newsapi_scrape")
    parsedArticles = []
    authors = set()
    sites = smallNews.split(',')

    for newsSite in sites:
        all_articles = newsapi.get_everything(language='en',sort_by='relevancy',sources=newsSite)

        for thing in all_articles:
            articleObjects = all_articles[thing]

            if (len(str(articleObjects))<10):
                continue

            for article in articleObjects:
                    entry = NewsApiArticle()
                    entry.source = newsSite.replace('-',' ')
                    entry.author = article['author']
                    entry.title = article['title']
                    entry.description = article['description']
                    entry.url = article['url']
                    entry.published = article['publishedAt'] #date
                    entry.content = article['content']
                    if(entry.content == None):
                        continue

                    url = str(entry.url)
                    art = Article(url)
                    art.download()
                    try:
                        art.parse()
                    except:
                        continue
                    art.nlp()
                    topicString = ",".join(art.keywords)
                    entry.topics = topicString
                    entry.wordCount = len(art.text.split())
                    if(entry.wordCount == 0):
                        continue
                    if(entry.author == None or 'www' in entry.author):
                        continue
                    try:
                        authorUrl = getAuthUrl(entry.author.split(',')[0])
                        singleAuthor = scrapeAuthorInfo(authorUrl.strip('articles'))
                        authors.add(singleAuthor)
                    except:
                        pass
                    parsedArticles.append(entry)
    return parsedArticles, authors