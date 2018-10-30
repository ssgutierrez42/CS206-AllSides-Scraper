import urllib2
from bs4 import BeautifulSoup

## Model Classes
#Featured Info
class FeatureThumb:
    title = ""
    link = ""
    political_side = ""
    source = ""

class FeaturedBlock:
    title = ""
    link = ""
    description = ""
    featureThumbs = []

#Column Info
class DailyArticle:
    title = ""
    topic = ""
    link = ""
    description = ""
    political_side = ""
    source = ""

## Script Variables
#AllSides
all_sides_balanced = 'https://www.allsides.com/unbiased-balanced-news' #HomePage
all_sides_balanced_html = urllib2.urlopen(all_sides_balanced)
all_sides_soup = BeautifulSoup(all_sides_balanced_html, 'html.parser')

#FeaturedBlocks
featuredBlocks = []
dailyArticles = []

def clean_bias_rating(rawRating):
    return rawRating.replace("Political News Media Bias Rating:", "").strip()

## Script Functions
def scrape_featured_blocks():
    featured_block_tag = 'block-views-story-id-single-story-block'
    featured_blocks = all_sides_soup.find_all(id=lambda value: value and value.startswith(featured_block_tag))

    counter = 0
    for featured_block in featured_blocks:
        block = FeaturedBlock()
        block.featureThumbs = []

        title_soup = featured_block.find('h2',class_='story-title').find('a')
        block.link = title_soup['href']
        block.title = title_soup.text

        description_soup = featured_block.find('div',class_='story-description').find('a')
        block.description = description_soup.text

        #feature-thumbs (three other thumbnail article suggestions)
        feature_thumbs_soup = featured_block.find_all('div',class_='feature-thumbs')
        for feature_soup in feature_thumbs_soup:
            thumb = FeatureThumb()

            title_soup = feature_soup.find('div',class_='news-title').find('a')
            thumb.title = title_soup.text
            thumb.link = title_soup['href']

            #political_side_soup = feature_soup.find('div',class_='global-bias')
            #thumb.political_side = political_side_soup.text
            # ^ using img tag below to obtain political side information (left,right,center)

            source_area_soup = feature_soup.find('div',class_='source-area')
            source_img = source_area_soup.find('img')
            thumb.political_side = clean_bias_rating(source_img['title'])
            source_soup = source_area_soup.find('a')
            thumb.source = source_soup.text

            block.featureThumbs.append(thumb)

        featuredBlocks.append(block)

def scrape_columns():
    daily_row_tag = 'allsides-daily-row'
    daily_rows = all_sides_soup.find_all('div', class_=daily_row_tag)

    for row in daily_rows:
        article = DailyArticle()

        title_soup = row.find('div',class_='news-title').find('a')
        article.title = title_soup.text
        article.link = title_soup['href']

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

        dailyArticles.append(article)

def printResult():
    print "BLOCKS"
    for block in featuredBlocks:
        print "Headline:"
        print block.title
        print block.description
        print block.link
        print "\n-----\n"
        print "Thumbnails:"
        for thumb in block.featureThumbs:
            print thumb.title
            print thumb.link
            print "SOURCE: " + thumb.source
            print "SIDE: " + thumb.political_side
            print "\n"
        print "\n\n"

    print "ARTICLES"
    for article in dailyArticles:
        print "Article"
        print "Title: " + article.title
        print "Topic: " + article.topic
        print "Desc: " + article.description
        print article.source
        print article.link
        print article.political_side
        print "\n\n"

## On runtime, do this:
def main():
    scrape_featured_blocks()
    scrape_columns()
    printResult()

main()
