import requests
from bs4 import BeautifulSoup
import cloudscraper
from .models import Source, News
import dateutil.parser


def update_feed_function():
    print("updating feed")

''''
def update_feed_function():
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
        except:
            continue
    #print(all_news)
    add_to_database(all_news)
    print("Done")


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
    #return HttpResponse(godd)
    for i in feed_list:
        the_url = getimage(i['link'], scraper)
        i['image_link'] = the_url

    return feed_list


def getimage(news_url, scraper):
    #scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
    info = scraper.get(news_url).text
    soup = BeautifulSoup(info, "html.parser")
    try:
        image_prop = soup.head.find(property="og:image")
        image_link = image_prop.get('content')
        print(image_link)
    except:
        image_link = 'https://fastly.picsum.photos/id/119/3264/2176.jpg?hmac=PYRYBOGQhlUm6wS94EkpN8dTIC7-2GniC3pqOt6CpNU'
        print(image_link)
    return image_link
    
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
            #print(i.get('title'))

'''
