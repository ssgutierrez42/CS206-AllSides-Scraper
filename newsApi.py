from newsapi import NewsApiClient
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
#NewsList = bigNews or smallNews
def scrape(newsList):
	all_articles = newsapi.get_everything(language='en',
	                                      sort_by='relevancy',
	                                      sources=newsList)

	for thing in all_articles:
		text = all_articles[thing]
		if(len(str(text))<10):
			continue
		for article in text:
			source = article['source']['name']
			author = article['author']
			title = article['title']
			description = article['description']
			url = article['url']
			published = article['publishedAt']
			content = article['content']
			wordCount = len(content.split(' '))
	return (source,author,title,description,url,published,content,wordCount)