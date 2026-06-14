from django.test import TestCase
from django.utils import timezone

from .models import Source, News, Subscriber


class ModelStrTests(TestCase):
    """The __str__ methods are used in the Django admin, so they should be stable."""

    def test_source_str_returns_title(self):
        source = Source.objects.create(
            source_title="Sample Source",
            source_url="https://example.com/rss",
        )
        self.assertEqual(str(source), "Sample Source")

    def test_news_str_returns_title(self):
        article = News.objects.create(
            title="Breaking Headline",
            link="https://example.com/article",
            date=timezone.now(),
            image_link="https://example.com/image.jpg",
        )
        self.assertEqual(str(article), "Breaking Headline")

    def test_subscriber_str_returns_email(self):
        subscriber = Subscriber.objects.create(suscribers_email="reader@example.com")
        self.assertEqual(str(subscriber), "reader@example.com")


class HomeViewTests(TestCase):
    def setUp(self):
        # Create more than one page worth of articles (the home view paginates by 12).
        for i in range(15):
            News.objects.create(
                title=f"Article {i}",
                link=f"https://example.com/{i}",
                date=timezone.now(),
                image_link="https://example.com/image.jpg",
            )

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_paginates_to_twelve(self):
        response = self.client.get("/")
        self.assertEqual(len(response.context["page_obj"]), 12)

    def test_home_page_orders_newest_first(self):
        page_obj = self.client.get("/").context["page_obj"]
        dates = [article.date for article in page_obj]
        self.assertEqual(dates, sorted(dates, reverse=True))


class SearchViewTests(TestCase):
    def setUp(self):
        News.objects.create(
            title="Lagos traffic update",
            link="https://example.com/lagos",
            date=timezone.now(),
            image_link="https://example.com/image.jpg",
        )
        News.objects.create(
            title="Abuja weather report",
            link="https://example.com/abuja",
            date=timezone.now(),
            image_link="https://example.com/image.jpg",
        )

    def test_search_filters_by_keyword(self):
        response = self.client.get("/search/", {"search_words": "Lagos"})
        self.assertEqual(response.status_code, 200)
        titles = [article.title for article in response.context["page_obj"]]
        self.assertIn("Lagos traffic update", titles)
        self.assertNotIn("Abuja weather report", titles)


class ClickTrackingTests(TestCase):
    def test_click_increments_counter_and_redirects(self):
        article = News.objects.create(
            title="Trackable article",
            link="https://example.com/destination",
            date=timezone.now(),
            image_link="https://example.com/image.jpg",
        )
        self.assertEqual(article.clicks, 0)

        response = self.client.get(f"/clicked/{article.id}/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://example.com/destination")
        article.refresh_from_db()
        self.assertEqual(article.clicks, 1)


class SubscribeTests(TestCase):
    def test_subscribe_stores_email_once(self):
        # First submission saves the email.
        self.client.post("/about/", {"email_address": "reader@example.com"})
        self.assertEqual(
            Subscriber.objects.filter(suscribers_email="reader@example.com").count(), 1
        )

        # Duplicate submission must not create a second record.
        self.client.post("/about/", {"email_address": "reader@example.com"})
        self.assertEqual(
            Subscriber.objects.filter(suscribers_email="reader@example.com").count(), 1
        )
