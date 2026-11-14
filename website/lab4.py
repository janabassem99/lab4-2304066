"""Lab 4 read-only reports, sharing the library's MySQL connection helper."""
from flask import Blueprint, render_template, request
from library import database, valid_price, positive_id
from lab4_queries import QUERIES, SEARCH

lab4 = Blueprint('lab4', __name__)


def rows(sql, parameters=()):
    with database() as connection, connection.cursor() as cursor:
        cursor.execute(sql, parameters)
        return list(cursor.fetchall())


@lab4.route('/')
@lab4.route('/search')
def search():
    categories = rows('SELECT category_id, name FROM CATEGORY ORDER BY name')
    error = None
    books = []
    try:
        keyword = request.args.get('keyword', '').strip()
        minimum = valid_price(request.args.get('minimum') or '0')
        maximum = valid_price(request.args.get('maximum') or '99999999.99')
        if minimum > maximum:
            raise ValueError('Minimum price must not exceed maximum price.')
        category = request.args.get('category', '')
        category_id = positive_id(category, 'Category') if category else None
        # Bonus: user values are passed separately; never concatenate them into SQL.
        books = rows(SEARCH, ('%' + keyword + '%', minimum, maximum, category_id, category_id))
    except ValueError as exc:
        error = str(exc)
    return render_template('lab4.html', title='Find your next book.', subtitle='Search by title, price and category.',
                           active='search', categories=categories, error=error,
                           sections=[('Matching books', books)])


PAGES = {
    'catalogue': ('The complete catalogue.', 'Books and the people behind them.', [('All books', 'catalogue')]),
    'reports': ('A closer look.', 'Category totals, authors and library prices.', [('Books by category', 'category_report'), ('Authors with at least two books', 'prolific'), ('Library prices', 'prices')]),
    'loans': ('Borrowed and waiting.', 'Current loans and books still waiting for their first reader.', [('Not returned yet', 'active_loans'), ('Members with no loans', 'no_members'), ('Books never borrowed', 'no_books')]),
    'popular': ('Reader favourites.', 'Each loan counts as one borrowing. Ties use the smallest ID first.', [('Three most borrowed books', 'top_books'), ('Member with the most loans', 'top_member')]),
    'authors': ('Meet the authors.', 'Every author counts, even before their first book is added.', [('All authors and their book counts', 'authors'), ('Author and publisher from the same country', 'same_country')]),
}


@lab4.route('/<page>')
def report(page):
    from flask import abort
    if page not in PAGES:
        abort(404)
    title, subtitle, definitions = PAGES[page]
    sections = [(heading, rows(QUERIES[key])) for heading, key in definitions]
    return render_template('lab4.html', title=title, subtitle=subtitle, active=page, sections=sections)


@lab4.route('/discussion')
def discussion():
    return render_template('lab4_discussion.html')
