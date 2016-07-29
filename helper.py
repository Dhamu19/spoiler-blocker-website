import config
import json
from flask import request, jsonify
from datetime import datetime, timedelta


def full_text_search(query, page_no, cur):
    offset = (page_no - 1) * config.ROWS_PER_PAGE

    count = -1
    if page_no == 1:
        cur.execute(
            "SELECT COUNT(*) FROM spoiler_lists WHERE (title ILIKE %s)",
            ('%' + query + '%',)
        )
        count = cur.fetchone()['count']

    # If empty query, return all rows
    if query == '':
        cur.execute(
            "SELECT id, title, tags, rating, num_downloads FROM spoiler_lists ORDER BY rating DESC LIMIT %s OFFSET %s",
            (config.ROWS_PER_PAGE, offset)
        )
        results = map(dict, cur.fetchall())
    else:
        results = []
        # Use id_set to ensure no lists are duplicated in results
        id_set = set()
        # One query for titles starting with query and one for titles containing
        # query in any form
        search_rows(results, id_set, query + '%', config.ROWS_PER_PAGE, offset, cur)
        search_rows(results, id_set, '%' + query + '%', config.ROWS_PER_PAGE, offset, cur)

    return results, count


# Return row data matching a query for populating a page with results
def search_rows(results, id_set, query, limit, offset, cur):
    cur.execute(
        "SELECT id, title, tags, rating, num_downloads FROM spoiler_lists WHERE (title ILIKE %s) ORDER BY rating DESC LIMIT %s OFFSET %s",
        (query, limit, offset)
    )

    check_duplicates(results, id_set, cur)


def full_title_search(query, cur):
    results = []
    id_set = set()
    # One query for titles starting with query and one for titles containing
    # query in any form
    search_titles(results, id_set, query + '%', cur)
    search_titles(results, id_set, '%' + query + '%', cur)

    return map(lambda x: x['title'], results)


# Return titles matching a query for autocomplete query
def search_titles(results, id_set, query, cur):
    cur.execute(
        "SELECT title, id FROM spoiler_lists WHERE (title ILIKE %s) LIMIT %s",
        (query, config.AUTCOMPLETE_MAX_ROWS)
    )

    check_duplicates(results, id_set, cur)


def check_duplicates(results, id_set, cur):
    for result in cur.fetchall():
        result_dict = dict(result)
        # If not a duplicate, add to results
        # and update id_set
        if result_dict['id'] not in id_set:
            results.append(result_dict)
            id_set.add(result_dict['id'])


def set_cookie(list_ID, userRating, ratingDict, conn, cur):
    is_new_rating = True
    cookie = json.loads(request.cookies.get('ratings', "{}"))

    if (request.cookies.get('ratings')) is None:
        is_new_rating = True
    else:
        if list_ID in cookie:
            is_new_rating = False
        else:
            is_new_rating = True

    if is_new_rating:
        # First time user is rating this list
        newNumRatings = ratingDict['num_ratings'] + 1
        newRating = (ratingDict['rating'] * ratingDict['num_ratings'] + userRating) / newNumRatings
    else:
        # User is updating his rating
        newNumRatings = ratingDict['num_ratings']
        newRating = (ratingDict['rating'] * ratingDict['num_ratings'] - cookie[list_ID] + userRating) / newNumRatings

    cur.execute(
        'UPDATE spoiler_lists SET rating=%s, num_ratings=%s WHERE id=%s',
        (newRating, newNumRatings, list_ID)
    )
    conn.commit()

    response = jsonify(newRating=newRating)
    # Set a large expire date to prevent users from
    # simply closing browser and opening it back up
    expire_date = datetime.now() + timedelta(weeks=100)
    # Update cookie to reflect the new userRating
    cookie[list_ID] = userRating
    response.set_cookie('ratings', json.dumps(cookie), expires=expire_date)

    return response
