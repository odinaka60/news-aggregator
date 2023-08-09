from django.db import models

# Create your models here.
class Source(models.Model):
    source_title = models.CharField(max_length=30)
    source_url = models.URLField(max_length = 200)
    home_url = models.URLField(max_length = 200, default='https://fastly.picsum.photos/id/119/3264/2176.jpg?hmac=PYRYBOGQhlUm6wS94EkpN8dTIC7-2GniC3pqOt6CpNU')
    source_category = models.CharField(max_length = 200, default='News')
    source_svg_link = models.URLField(max_length = 200, default='https://fastly.picsum.photos/id/119/3264/2176.jpg?hmac=PYRYBOGQhlUm6wS94EkpN8dTIC7-2GniC3pqOt6CpNU')
    
    def __str__(self):
        return self.source_title
    

class News(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length = 200)
    date = models.DateTimeField()
    image_link = models.URLField(max_length = 200)
    name = models.CharField(max_length=255, default='Online News')
    favi_link = models.URLField(max_length = 200, default='https://ibb.co/n7bVQjR')
    category = models.CharField(max_length=255, default='News')
    clicks = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
class Subscriber(models.Model):
    suscribers_email = models.EmailField()
    
    def __str__(self):
        return self.suscribers_email