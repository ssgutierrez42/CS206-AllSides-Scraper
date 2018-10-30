import urllib2
from bs4 import BeautifulSoup


## Model Classes
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

## Script Variables
#AllSides
all_sides_balanced = 'https://www.allsides.com/unbiased-balanced-news' #HomePage
all_sides_balanced_html = urllib2.urlopen(all_sides_balanced)
all_sides_soup = BeautifulSoup(all_sides_balanced_html, 'html.parser')

#FeaturedBlocks
featuredBlocks = []

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

            political_side_soup = feature_soup.find('div',class_='global-bias')
            thumb.political_side = political_side_soup.text

            source_side_soup = feature_soup.find('div',class_='source-area').find('a')
            thumb.source = source_side_soup.text

            block.featureThumbs.append(thumb)

        featuredBlocks.append(block)

def scrape_columns():
    print ""

## On runtime, do this:
scrape_featured_blocks()
scrape_columns()

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
