# Odithe News — Nigerian News Aggregator

A full-stack Django web application that aggregates the latest headlines from multiple Nigerian news outlets into a single, searchable feed. News is collected automatically by a scheduled scraping pipeline that pulls from each source's RSS feed, enriches every article with its cover image, de-duplicates, and stores it in the database for fast browsing.

**Live site:** https://www.odithenews.com/

> Built and deployed to production while I was based in Nigeria. The project is live and self-updating via scheduled jobs.

---

## Tech Stack

| Area | Tools |
|------|-------|
| Backend | Python 3.10, Django 4.2 |
| Scraping | BeautifulSoup4, cloudscraper (Cloudflare bypass), requests, lxml |
| Database | SQLite (dev), PostgreSQL / MySQL (production-ready) |
| Frontend | Django templates, Bootstrap 5, responsive layout |
| Deployment | Gunicorn, WhiteNoise (static files), PythonAnywhere with cron-scheduled jobs |
| Config | django-environ / python-dotenv for environment-based secrets |

---

## Key Features

- **Automated scraping pipeline** — a custom Django management command (`updatefeed`) iterates over registered sources, parses their RSS feeds, scrapes each article page for its Open Graph cover image, and inserts new records while skipping duplicates.
- **Scheduled, hands-off updates** — the pipeline runs at intervals via cron, keeping the feed current without manual intervention.
- **Self-maintaining database** — a `cleardb` command prunes the oldest articles once the table exceeds a configurable limit, keeping storage bounded.
- **Search** — full-text-style filtering of headlines by keyword.
- **Category browsing** — articles are grouped and filterable by source category.
- **Pagination** — 12 headlines per page across all listing views.
- **Click tracking** — each outbound click is counted before redirecting to the original article.
- **Email features** — newsletter subscription capture and a working contact form (Django email backend).
- **Responsive UI** — mobile-friendly and adapts across screen sizes.

---

## Architecture at a Glance

```
RSS feeds (multiple Nigerian sources)
        │
        ▼
updatefeed (Django management command, run on a cron schedule)
  ├─ parse feed items with BeautifulSoup (XML)
  ├─ scrape each article page for its og:image
  └─ de-duplicate + save to DB
        │
        ▼
   News model  ──►  Django views (home / search / category / share)
        │
        ▼
   Bootstrap templates  ──►  odithenews.com
```

Core models: `Source` (a feed and its metadata), `News` (an aggregated article), and `Subscriber` (newsletter emails).

---

## Running Locally

```bash
# 1. Clone and enter the project
git clone <repo-url>
cd news-aggregator

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables (see .env.example)
cp .env.example .env            # then fill in the email settings

# 5. Apply migrations
python manage.py migrate

# 6. Create an admin user to register news sources
python manage.py createsuperuser

# 7. Start the dev server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. Add one or more sources in the Django admin (`/admin`), each with an RSS feed URL, then populate the feed:

```bash
python manage.py updatefeed     # scrape sources and store articles
python manage.py cleardb        # prune oldest articles past the limit
```

In production these two commands are scheduled with cron so the feed refreshes automatically.

### Running the tests

The test suite runs against an in-memory SQLite database (no MySQL server required):

```bash
python manage.py test --settings=newsfeed.test_settings
```

It covers the data models and the core views — home pagination and ordering, keyword search, click tracking, and de-duplicated newsletter sign-ups.

---

## What I Learned

- Designing and operating a **scheduled data pipeline** end to end — fetching, parsing, enriching, de-duplicating, and persisting third-party data.
- Handling the realities of scraping live sites: **Cloudflare protection** (cloudscraper), inconsistent feed formats, missing images, and per-source failures handled gracefully so one bad feed doesn't break the run.
- Building and **deploying a Django app to production** with Gunicorn, WhiteNoise, environment-based configuration, and scheduled jobs.
- Implementing common product features from scratch: pagination, search, categorisation, click analytics, and transactional email.

---

## Possible Improvements

This was an early project, and with more time I would: add automated tests around the scraping and views, move source de-duplication to a database-level constraint, replace bare `except` blocks with targeted error handling and logging, and add an async task queue (e.g. Celery) in place of cron for more robust scheduling.
