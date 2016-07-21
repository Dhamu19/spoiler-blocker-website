import os
import psycopg2
import psycopg2.extras
import urlparse

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

def fullTextSearch(search):
    # cur.execute(
    #     "SELECT id, title, tags FROM ( \
    #          SELECT id, title, tags, tsv \
    #          FROM block_lists, plainto_tsquery(%s) AS q \
    #          WHERE (tsv @@ q) \
    #      ) AS t1 ORDER BY ts_rank_cd(t1.tsv, plainto_tsquery(%s)) DESC LIMIT 5;",
    #     (search, search)
    # )
    if search == '':
        cur.execute("SELECT id, title, tags, rating, num_downloads FROM block_lists;")
        return map(dict, cur.fetchall())
    else:
        results = []
        idSet = set()
        searchLists(results, idSet, 'title', search + '%')
        searchLists(results, idSet, 'title', '%' + search + '%')
        searchLists(results, idSet, 'tags', '%' + search + '%')

    return results

def searchLists(results, idSet, column, search):
    selectLists(column, search)
    for result in cur.fetchall():
        resultDict = dict(result)
        if resultDict['id'] not in idSet:
            results.append(resultDict)
            idSet.add(resultDict['id'])

def selectLists(column, search):
    cur.execute(
        "SELECT id, title, tags, rating, num_downloads FROM block_lists WHERE (" + column + " ILIKE %s) LIMIT 10",
        (search,)
    )
