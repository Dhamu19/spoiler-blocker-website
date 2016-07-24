import psycopg2
import psycopg2.extras
import urlparse
import os

# Database connection
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
