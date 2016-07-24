from db_connector import cur
import config


def full_text_search(search):
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
        id_set = set()
        search_lists(results, id_set, 'title', search + '%')
        search_lists(results, id_set, 'title', '%' + search + '%')

    return results


def search_lists(results, id_set, column, search):
    select_lists(column, search, config.ROWS_PER_PAGE)
    for result in cur.fetchall():
        result_dict = dict(result)
        if result_dict['id'] not in id_set:
            results.append(result_dict)
            id_set.add(result_dict['id'])


# Return row data matching a query for populating a page with results
def select_lists(column, search, limit, page_no):
    offset = (page_no - 1) * limit

    cur.execute(
        "SELECT id, title, tags, rating, num_downloads FROM block_lists WHERE (%s ILIKE %s) LIMIT %s ORDER BY rating OFFSET %s",
        (column, search, limit, offset)
    )


# Return titles matching a search query for autocomplete search
def select_titles(search, limit):
    cur.execute(
        "SELECT title FROM block_lists WHERE (title ILIKE %s) LIMIT %s",
        (search, limit)
    )
