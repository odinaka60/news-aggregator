from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about),
    path('contact/', views.contact),
    path('share/<str:id>/', views.share),
    path('search/', views.search),
    path('category/<str:value>/', views.category),
    path('clicked/<str:no>/<path:link>/', views.clicked),
]