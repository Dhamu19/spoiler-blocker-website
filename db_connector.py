import psycopg2
import psycopg2.extras
import urlparse
import os

# Database connection
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])


def db_connection():
    return psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )


def db_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
