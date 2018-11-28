from newsapi.newsapi_client import NewsApiClient

import string
from newspaper import Article

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

class NewsApiArticle:
    source = ""
    author = ""
    title = ""
    description = ""
    url = ""
    published = ""
    content = ""
    wordCount = ""
    topic = ""

#NewsList = bigNews or smallNews

def newsapi_scrape():
    print("newsapi_scrape")
    all_articles = newsapi.get_everything(language='en',sort_by='relevancy',sources=smallNews)

    parsedArticles = []

    for thing in all_articles:
        articleObjects = all_articles[thing]

        if (len(str(articleObjects))<10):
            continue

        for article in articleObjects:
            entry = NewsApiArticle()

            #print(article)

            entry.source = article['source']['name']
            entry.author = article['author']
            entry.title = article['title']
            entry.description = article['description']
            entry.url = article['url']
            entry.published = article['publishedAt'] #date
            entry.content = article['content']

            if entry.content is not None:
                entry.wordCount = len(entry.content.split(' '))

            parsedArticles.append(entry)

    return parsedArticles
