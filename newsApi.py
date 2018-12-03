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
from IPython.display import HTML
#results = search('muckrack erik wemple')
#link = results[0][1]
buildargs = {
  'serviceName': 'customsearch',
  'version': 'v1',
  'developerKey': 'AIzaSyCdMqTmsONtYV8x4IHruTgIOQxzMAZRuBE'
}
subscription_key = "438df901be8e4b68b447d87071674860"
assert subscription_key
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
def getAuthUrl(author):
    search_term = "muckrack "+author
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return search_results["webPages"]["value"][0]['url']


    #cseargs = {'q': author,'cx': '002127797185034144380:9cz4vhqwpfq','num': 1}
    #results = search_google.api.results(buildargs, cseargs)
    #return results.links[0]


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

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

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
    top_headline = False

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
        all_articles_list = list()
        all_articles1 = newsapi.get_top_headlines(language='en',sources=newsSite)
        all_articles2 = newsapi.get_everything(language='en',sources=newsSite, sort_by = 'relevancy')
        all_articles_list.append(all_articles1)
        all_articles_list.append(all_articles2)
        for all_articles in all_articles_list:
            if(all_articles == all_articles_list[0]):
                top_h = True
            else:
                top_h = False
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
                        entry.top_headline = top_h
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