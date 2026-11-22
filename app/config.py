import os
from dotenv import load_dotenv

load_dotenv()

# Mastodon
MASTODON_BASE_URL = os.getenv("MASTODON_BASE_URL", "").rstrip("/")
MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN", "")

# Bluesky
BLUESKY_IDENTIFIER = os.getenv("BLUESKY_IDENTIFIER", "")
BLUESKY_APP_PASSWORD = os.getenv("BLUESKY_APP_PASSWORD", "")
BLUESKY_HANDLE = os.getenv("BLUESKY_HANDLE", "")

# Reddit
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "")
REDDIT_SUBREDDIT = os.getenv("REDDIT_SUBREDDIT", "")
REDDIT_USER_AGENT = os.getenv(
    "REDDIT_USER_AGENT",
    "AutomatedPostingSystem/1.0"
)

# WordPress
WORDPRESS_SITE_URL = os.getenv("WORDPRESS_SITE_URL", "").rstrip("/")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME", "")
WORDPRESS_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD", "")

# LinkedIn
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_PERSON_ID = os.getenv("LINKEDIN_PERSON_ID", "")
LINKEDIN_VERSION = os.getenv("LINKEDIN_VERSION", "202611")