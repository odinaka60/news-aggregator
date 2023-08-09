from django.contrib import admin
from .models import Source, News, Subscriber

# Register your models here.
admin.site.register(Source)
admin.site.register(News)
admin.site.register(Subscriber)