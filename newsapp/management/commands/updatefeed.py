import requests
from bs4 import BeautifulSoup
import cloudscraper
from newsapp.models import Source, News
import dateutil.parser
from django.core.management.base import BaseCommand


''''
def update_feed_function():
    print("updating feed")
'''

#function that fetch news articles from the rss feed of different sources
def getnews(url, favicon_link, name_title, name_category):
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
    URL = url
    info = scraper.get(URL).text

    soup = BeautifulSoup(info, "xml")
    source_name = soup.channel.title.string
    print(source_name)
    feeds = soup.find_all('item')
    feed_list = []
    for feed in feeds:
        feed_details = {'title':feed.title.string, 'link': feed.link.string, 'date': dateutil.parser.parse(feed.pubDate.string), 'name': name_title, 'favi_link': favicon_link, 'category': name_category}
        feed_list.append(feed_details)
    for i in feed_list:
        the_url = getimage(i['link'], scraper)
        i['image_link'] = the_url

    return feed_list

# function that fetch the news article images from the url
def getimage(news_url, scraper):
    info = scraper.get(news_url).text
    soup = BeautifulSoup(info, "html.parser")
    try:
        image_prop = soup.head.find(property="og:image")
        image_link = image_prop.get('content')
        print("image retrieval successfull")
    except:
        image_link = 'https://ibb.co/n7bVQjR'
        print("image retrieval not successfull, using default image")
    return image_link

#function that adds the news articles to database
def add_to_database(all_news):
    for i in all_news:
        the_title = i.get('title')
        the_link = i.get('link')
        the_date = i.get('date')
        the_image_link = i.get('image_link')
        the_name = i.get('name')
        the_favi_link = i.get('favi_link')
        the_category = i.get('category')
        if News.objects.filter(title=the_title):
            continue
        else:
            d = News(title=the_title, link=the_link, date=the_date, image_link=the_image_link, name=the_name, favi_link=the_favi_link, category=the_category)
            d.save()


class Command(BaseCommand):

    def handle(self, *args, **options):
        #function that updates the news feed
        feedurl_list = Source.objects.values_list('source_url', flat=True)
        all_news = []
        for i in feedurl_list:
            try:
                qeury_result = Source.objects.filter(source_url=i).first()
                favicon_link = qeury_result.source_svg_link
                name_title = qeury_result.source_title
                name_category = qeury_result.source_category
                result = getnews(i, favicon_link, name_title, name_category)
                all_news = all_news + result
            #except:
            except Exception as error:
                print(f"{i} not responding {error}")
                continue
        add_to_database(all_news)
        print("Done")
