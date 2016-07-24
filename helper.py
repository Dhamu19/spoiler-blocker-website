from db_connector import cur
import config


def full_text_search(query, page_no):
    offset = (page_no - 1) * config.ROWS_PER_PAGE

    count = None
    if page_no == 1:
        cur.execute("SELECT COUNT(*) FROM spoiler_lists WHERE (title ILIKE %s)", 
            ('%' + query + '%')
        )
        count = cur.fetchone()['count']

    # If empty query, return all rows
    if query == '':
        cur.execute("SELECT id, title, tags, rating, num_downloads FROM spoiler_lists LIMIT %s ORDER BY rating OFFSET %s",
            config.ROWS_PER_PAGE, offset
        )
        results = map(dict, cur.fetchall())
    else:
        results = []
        id_set = set()
        search_rows(results, id_set, query + '%', config.ROWS_PER_PAGE, offset)
        search_rows(results, id_set, '%' + query + '%', config.ROWS_PER_PAGE, offset)

    return results, count


# Return row data matching a query for populating a page with results
def search_rows(results, id_set, query, limit, offset):
    cur.execute(
        "SELECT id, title, tags, rating, num_downloads FROM spoiler_lists WHERE (title ILIKE %s) LIMIT %s ORDER BY rating OFFSET %s",
        (query, limit, offset)
    )
    check_duplicates(results, id_set)


def full_title_search(query):
    results = []
    id_set = set()
    search_titles(results, id_set, query + '%')
    search_titles(results, id_set, '%' + query + '%')

    return map(lambda x: x['title'], results)


# Return titles matching a query for autocomplete query
def search_titles(results, id_set, query):
    cur.execute(
        "SELECT title, id FROM block_lists WHERE (title ILIKE %s) LIMIT %s",
        (query, config.AUTCOMPLETE_MAX_ROWS)
    )

    check_duplicates(results, id_set)


def check_duplicates(results, id_set):
    for result in cur.fetchall():
        result_dict = dict(result)
        if result_dict['id'] not in id_set:
            results.append(result_dict)
            id_set.add(result_dict['id'])
