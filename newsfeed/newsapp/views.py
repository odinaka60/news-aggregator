from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import cloudscraper
from .models import Source, News, Subscriber
import dateutil.parser
from .forms import SearchForm, ContactForm, SubscribeForm
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
source_category_list = Source.objects.values_list('source_category', flat=True)
source_category_list = list(set(source_category_list))
home_url_list = Source.objects.values_list('home_url', flat=True)
svg_list = Source.objects.values_list('source_svg_link', flat=True)


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
                'form': form, }
    #context = {'news': news}
    return render(request, "home.html", context)

def about(request):
    subscribe_form = SubscribeForm()
    if request.method == "POST":
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            email_address = subscribe_form.cleaned_data["email_address"]
            if Subscriber.objects.filter(suscribers_email=email_address):
                print("Email already exist")
            else:
                b = Subscriber(suscribers_email=email_address)
                b.save()
                print(email_address)
    context = {'subscribe_form': subscribe_form}
    return render(request, "about.html", context)

def contact(request):
    contact_form = ContactForm()
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            try:
                subject = contact_form.cleaned_data["subject"]
                message = contact_form.cleaned_data["message"]
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [settings.EMAIL_HOST_USER, ]
                send_mail( subject, message, email_from, recipient_list)
                print('email sent')
                return redirect('/contact/')
            except:
                print( 'email not sent')
                return redirect('/contact/')
    context = {'contact_form': contact_form}
    return render(request, "contact.html", context)

def share(request, id):
    news = News.objects.order_by('-date')[:6]
    shared_news = News.objects.get(id=id)
    context = {'news': news, 'shared_news': shared_news}
    return render(request, "sharepage.html", context)

def clicked(request, no, link):
    clicked_news = News.objects.get(id=no)
    new_click_value= clicked_news.clicks+1
    News.objects.filter(id=no).update(clicks=new_click_value)
    return redirect(link)

def search(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            search_words = form.cleaned_data["search_words"]
            #print(search_words)
            
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
    return render(request, "category.html", context)  
    

