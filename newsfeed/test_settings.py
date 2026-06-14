"""Test-only settings.

Inherits everything from the main settings module but swaps the production
MySQL database for an in-memory SQLite database so the test suite can run
without a database server. Run with:

    python manage.py test --settings=newsfeed.test_settings
"""

from .settings import *  # noqa: F401,F403

SECRET_KEY = "test-secret-key-not-for-production"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Avoid WhiteNoise's manifest storage during tests (no collectstatic run).
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Keep emails out of the network during tests.
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
