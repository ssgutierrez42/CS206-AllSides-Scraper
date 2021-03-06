## Imports
from articleScraper import scrape_article
from articleScraper import OpenArticle
from newsApi import newsapi_scrape
from newsApi import NewsApiArticle

from datetime import datetime

#RDS
import secrets

#Scraping
import requests
from bs4 import BeautifulSoup

#Database Connection
import pymysql

## Model Classes
#Featured Info
class FeaturedBlock:
    title = ""
    link = ""
    topic = ""
    description = ""
    political_side = "unbiased_balanced"
    source = "AllSides"
    opinionArticles = []

#Column Info
class DailyArticle:
    title = ""
    topic = ""
    link = ""
    description = ""
    political_side = ""
    source = ""

class AuthorInformation:
    name = ""
    location = ""
    title = ""
    beats = ""
    description = ""

## Script Variables
#AllSides
all_sides_balanced = 'https://www.allsides.com/unbiased-balanced-news' #HomePage
all_sides_balanced_html = requests.get(all_sides_balanced).text
all_sides_soup = BeautifulSoup(all_sides_balanced_html, 'html.parser')

#FeaturedBlocks
featuredBlocks = []
dailyArticles = []

# Connect to DB
username = secrets.db_username
password = secrets.db_password
db_name = secrets.db_name
rds_host = secrets.host
try:
    db_conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

def clean_bias_rating(rawRating):
    return rawRating.replace("Political News Media Bias Rating:", "").strip()

def clean_relative_url(url):
    if url.startswith('/'):
        return 'https://www.allsides.com' + url
    return url

def exists_in_articles(link):
    with db_conn.cursor() as cur:
        cur.execute("SELECT link, COUNT(*) FROM articles WHERE link = %s GROUP BY link",(link))
        if cur.rowcount != 0:
            print("Headline already exists, so skipping.")
            return True
    return False

## Script Functions
def scrape_featured_blocks():
    featured_block_tag = 'block-views-story-id-single-story-block'
    featured_blocks = all_sides_soup.find_all(id=lambda value: value and value.startswith(featured_block_tag))

    for featured_block in featured_blocks:
        block = FeaturedBlock()
        block.opinionArticles = []

        title_soup = featured_block.find('h2',class_='story-title').find('a')
        block.link = clean_relative_url(title_soup['href'])
        block.title = title_soup.text

        description_soup = featured_block.find('div',class_='story-description').find('a')
        block.description = description_soup.text

        _topic_soup = featured_block.find('div',class_='news-topic')
        if _topic_soup is not None:
            topic_soup = featured_block.find('div',class_='news-topic').find('a')
            block.topic = topic_soup.text

        #feature-thumbs (three other thumbnail article suggestions)
        feature_thumbs_soup = featured_block.find_all('div',class_='feature-thumbs')
        for feature_soup in feature_thumbs_soup:
            thumb = DailyArticle()
            thumb.topic = block.topic
            thumb.description = None

            title_soup = feature_soup.find('div',class_='news-title').find('a')
            thumb.title = title_soup.text
            thumb.link = clean_relative_url(title_soup['href'])

            #political_side_soup = feature_soup.find('div',class_='global-bias')
            #thumb.political_side = political_side_soup.text
            # ^ using img tag below to obtain political side information (left,right,center)

            source_area_soup = feature_soup.find('div',class_='source-area')
            source_img = source_area_soup.find('img')
            thumb.political_side = clean_bias_rating(source_img['title'])
            source_soup = source_area_soup.find('a')
            thumb.source = source_soup.text

            block.opinionArticles.append(thumb)

        featuredBlocks.append(block)

#scrape article columns on site (left, right, center)
def scrape_columns():
    daily_row_tag = 'allsides-daily-row'
    daily_rows = all_sides_soup.find_all('div', class_=daily_row_tag)

    for row in daily_rows:
        try:
            article = DailyArticle()

            title_soup = row.find('div',class_='news-title').find('a')
            article.title = title_soup.text
            article.link = clean_relative_url(title_soup['href'])

            topic_soup = row.find('div',class_='news-topic').find('a')
            article.topic = topic_soup.text

            source_soup = row.find('div',class_='news-source').find('a')
            article.source = source_soup.text

            bias_soup = row.find('div',class_='bias-container')
            bias_image = bias_soup.find('img')
            article.political_side = clean_bias_rating(bias_image['title'])

            body_soup = row.find('div',class_='news-body')
            paragraph_soup = body_soup.find('p')
            if paragraph_soup is not None:
                article.description = paragraph_soup.text
            elif body_soup.text is not None:
                article.description = body_soup.text.strip()
            else:
                article.description = None

            dailyArticles.append(article)
        except:
            continue

#add articles to database
def update_database_articles(articlesList, headlineId = None):
    if db_conn is None:
        return

    for index, article in enumerate(articlesList):
        print("Updating Article #" + str(index) + "/" + str(len(articlesList)))

        if exists_in_articles(article.link):
            print("Article already exists, so skipping.")
            continue

        now = datetime.utcnow()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        with db_conn.cursor() as cur:

            articlelink = article.link

            scrapedArticles = scrape_article([articlelink])
            articleInfo = scrapedArticles[0] if (len(scrapedArticles) > 0) else OpenArticle()

            if (articleInfo.authors is None) or (articleInfo.authors is ''):
                articleInfo.authors = article.source

            if article.description is None:
                article.description = article.title

            if (articleInfo.text is None) or (articleInfo.text is ''):
                if article.description is not None:
                    articleInfo.text = article.description
                else:
                    articleInfo.text = article.title

            #if (articleInfo.wordCount is 0) or (articleInfo.wordCount is None):
             #   articleInfo.wordCount = len(article.text.split())

            # print(articleInfo.authors)
            # print(articleInfo.date)

            cur.execute('insert into articles (created_at, updated_at, title, topic, description, link, side, source, wordcount, text, date_published, author) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE updated_at = %s', (formatted_date, formatted_date, article.title, article.topic, article.description, article.link, article.political_side, article.source, articleInfo.wordCount, articleInfo.text, articleInfo.date, articleInfo.authors, formatted_date))
            db_conn.commit()

            if headlineId is not None:
                relatedToId = cur.lastrowid
                print("Updating relations between " + str(headlineId) + " and " + str(relatedToId))

                cur.execute('insert into article_relations (article_id, related_to_id, relation_type) values(%s, %s, %s)', (headlineId, relatedToId, article.political_side))
                db_conn.commit()


def update_database_headlines(headlinesList):
    if db_conn is None:
        return

    for index, headline in enumerate(headlinesList):
        print("Updating Headline #" + str(index) + "/" + str(len(headlinesList)))

        if exists_in_articles(headline.link):
            print("Headline already exists, so skipping.")
            continue

        now = datetime.utcnow()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        with db_conn.cursor() as cur:

            if (headline.description is None) or (headline.description is ''):
                headline.description = headline.title

            _wordCount = len(headline.description.split())
            wordCount = _wordCount if (headline.description is not None) else None

            cur.execute('insert into articles (created_at, updated_at, title, topic, description, link, side, wordcount, source, author, text) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE updated_at = %s', (formatted_date, formatted_date, headline.title, headline.topic, headline.description, headline.link, headline.political_side, wordCount, headline.source, headline.source, headline.description, formatted_date))

            db_conn.commit()

            update_database_articles(headline.opinionArticles, cur.lastrowid)

def print_result():
    print("BLOCKS")
    for block in featuredBlocks:
        print("Headline:")
        print(block.title)
        print(block.description)
        print(block.link)
        print(block.topic)
        print("\n-----\n")
        print("Thumbnails:")
        for thumb in block.opinionArticles:
            print(thumb.title)
            print(thumb.link)
            print(thumb.topic)
            print("SOURCE: " + thumb.source)
            print("SIDE: " + thumb.political_side)
            print("\n")
        print("\n\n")

    print("ARTICLES")
    for article in dailyArticles:
        print("Article")
        print("Title: " + article.title)
        print("Topic: " + article.topic)
        print("Desc: " + article.description)
        print(article.source)
        print(article.link)
        print(article.political_side)
        print("\n\n")

def add_author_information(authors):
    print("Putting in Authors")
    for author in authors:
        if(author.name == ''):
            continue
        if db_conn is None:
            return
        with db_conn.cursor() as cur:
            now = datetime.utcnow()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            cur.execute('insert into authors (updated_at, name, location, job, beats, description) values(%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE updated_at = %s', (formatted_date, author.name, author.location, author.title, author.beats, author.description, formatted_date))
            db_conn.commit()

def scrape_from_newsapi():
    articles, authors = newsapi_scrape()
    for article in articles:
        if db_conn is None:
            return
        with db_conn.cursor() as cur:
            now = datetime.utcnow()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            cur.execute('insert into articles (created_at, date_published, topic, updated_at, title, description, link, wordcount, source, author, text, is_headline) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE updated_at = %s', (formatted_date, article.published, article.topics, formatted_date, article.title, article.description, article.url, article.wordCount, article.source, article.author, article.content, article.top_headline, formatted_date))
            db_conn.commit()
    add_author_information(authors)
        #TODO: store available details about article in DB here


## On runtime, do this:
def handler():
    all_sides_balanced_html = requests.get(all_sides_balanced).text
    all_sides_soup = BeautifulSoup(all_sides_balanced_html, 'html.parser')

    featuredBlocks.clear()
    dailyArticles.clear()

    scrape_featured_blocks()
    scrape_columns()
    #print_result()

    print("[DB] Updating Articles")
    update_database_articles(dailyArticles)

    print("[DB] Updating Featured Headlines")
    update_database_headlines(featuredBlocks)

    scrape_from_newsapi() #uncomment this when code is ready for production
handler()
#scrape_from_newsapi() #uncomment this for testing
