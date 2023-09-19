from newsapp.models import Source, News
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        # deleting old news in the database
        db_limit = 10000
        count = News.objects.filter().count()
        print(f'news database entries is {count} in number')
        if count > db_limit:
            extra = count - db_limit
            print(f'extra news database entries is {extra}')
            extra_news_id = News.objects.order_by('date')[:extra].values_list("id", flat=True)
            News.objects.filter(pk__in=list(extra_news_id)).delete()
            new_count = News.objects.filter().count()
            print(f'news database entries reduced to {new_count}')
        else:
            print(f'news database entries not more than {db_limit}')