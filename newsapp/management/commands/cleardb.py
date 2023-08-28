from newsapp.models import Source, News
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        # deleting old news in the database
        db_limit = 500
        count = News.objects.filter().count()
        print(f'news database entries is {count} in number')
        if count > db_limit:
            extra = count - db_limit
            news = News.objects.filter(pk__in = News.objects.order_by('date').values_list('pk')[:extra]).delete()
            print(f'news database entries reduced to {db_limit}')
        else:
            print(f'news database entries not more than {db_limit}')