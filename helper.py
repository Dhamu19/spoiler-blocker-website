from db_connector import cur
import config


def full_text_search(query, page_no):
    offset = (page_no - 1) * config.ROWS_PER_PAGE

    count = None
    if page_no == 1:
        cur.execute("SELECT COUNT(*) FROM block_lists WHERE (title ILIKE %s)", 
            ('%' + query + '%')
        )
        count = cur.fetchone()['count']

    # If empty query, return all rows
    if query == '':
        cur.execute("SELECT id, title, tags, rating, num_downloads FROM block_lists LIMIT %s ORDER BY rating OFFSET %s",
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
        "SELECT id, title, tags, rating, num_downloads FROM block_lists WHERE (title ILIKE %s) LIMIT %s ORDER BY rating OFFSET %s",
        (query, limit, offset)
    )

    for result in cur.fetchall():
        result_dict = dict(result)
        if result_dict['id'] not in id_set:
            results.append(result_dict)
            id_set.add(result_dict['id'])    


# Return titles matching a query for autocomplete query
def search_titles(query, limit):
    cur.execute(
        "SELECT title FROM block_lists WHERE (title ILIKE %s) LIMIT %s",
        (query, limit)
    )
