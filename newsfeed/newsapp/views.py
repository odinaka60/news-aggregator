from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import cloudscraper
from .models import Source, News
import dateutil.parser
from .forms import SearchForm


# Create your views here.
source_category_list = Source.objects.values_list('source_category', flat=True)
source_category_list = list(set(source_category_list))
home_url_list = Source.objects.values_list('home_url', flat=True)
svg_list = Source.objects.values_list('source_svg_link', flat=True)

#feedurl_list = ["https://www.vanguardngr.com/feed", "https://guardian.ng/feed/", "https://www.premiumtimesng.com/feed", "https://rss.punchng.com/v1/category/latest_news"]
def home(request):
    news = News.objects.order_by('-date')
    p = Paginator(news, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    form = SearchForm()
    context = {'page_obj': page_obj, 
                'source_category_list': source_category_list,
                'form': form, 
                "head_title": "home"}
    #context = {'news': news}
    return render(request, "home.html", context)

def about(request):
    return render(request, "about.html",)

def share(request, id):
    news = News.objects.order_by('-date')[:6]
    shared_news = News.objects.get(id=id)
    context = {'news': news, 'shared_news': shared_news}
    return render(request, "sharepage.html", context)

def search(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            search_words = form.cleaned_data["search_words"]
            print(search_words)
            
            searched_news = News.objects.filter(title__contains=search_words).order_by('-date')
            p = Paginator(searched_news, 12)
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)  # returns the desired page object
            except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
                page_obj = p.page(1)
            except EmptyPage:
                # if page is empty then return last page
                page_obj = p.page(p.num_pages)
            context = {'page_obj': page_obj, 'search_words': search_words, 'form': form}
            return render(request, "searchpage.html", context)
    
    
def category(request, value):
    category_news_result = News.objects.filter(category=value).order_by('-date')
    p = Paginator(category_news_result, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    form = SearchForm()
    context = {'page_obj': page_obj, 'value': value}
    #context = {'news': news}
    return render(request, "category.html", context)  
    

'''''
def home(request):
    feedurl_list = Source.objects.values_list('source_url', flat=True)
    all_news = []
    for i in feedurl_list:
        try:
            result = getnews(i)
            all_news = all_news + result
        except:
            continue
    context = {'headlines': all_news}
    #print(all_news)
    add_to_database(all_news)
    return render(request, "viewmodels.html", context)

def getnews(url):
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
    URL = url
    info = scraper.get(URL).text

    soup = BeautifulSoup(info, "xml")
    source_name = soup.channel.title.string
    print(source_name)
    feeds = soup.find_all('item')
    feed_list = []
    for feed in feeds:
        feed_details = {'title':feed.title.string, 'link': feed.link.string, 'date': dateutil.parser.parse(feed.pubDate.string), 'name': source_name}
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
        if News.objects.filter(title=the_title):
            continue
        else:
            d = News(title=the_title, link=the_link, date=the_date, image_link=the_image_link, name=the_name)
            d.save()
            #print(i.get('title'))
    
    
'''