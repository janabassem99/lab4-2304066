"""SQL used by Lab 4 pages. Inputs are passed separately as parameters."""

SEARCH = """SELECT b.book_id, b.title, b.price, c.name AS category
FROM BOOK b JOIN CATEGORY c ON b.category_id=c.category_id
WHERE b.title LIKE %s AND b.price BETWEEN %s AND %s
AND (%s IS NULL OR b.category_id=%s)
ORDER BY b.price ASC, b.book_id"""

QUERIES = {
    'catalogue': """
SELECT b.book_id, b.title, b.price, b.publish_year, a.name AS author, p.name AS publisher, c.name AS category
FROM BOOK b JOIN AUTHOR a ON b.author_id=a.author_id
JOIN PUBLISHER p ON b.publisher_id=p.publisher_id
JOIN CATEGORY c ON b.category_id=c.category_id ORDER BY b.title, b.book_id
""",
    'category_report': """
SELECT c.category_id, c.name AS category, COUNT(b.book_id) AS books, AVG(b.price) AS average_price
FROM CATEGORY c LEFT JOIN BOOK b ON b.category_id=c.category_id
GROUP BY c.category_id, c.name ORDER BY c.name
""",
    'prolific': """
SELECT a.author_id, a.name AS author, COUNT(b.book_id) AS books
FROM AUTHOR a JOIN BOOK b ON b.author_id=a.author_id
GROUP BY a.author_id, a.name HAVING COUNT(b.book_id)>=2 ORDER BY books DESC, a.author_id
""",
    'prices': """
SELECT SUM(price) AS total_price, MIN(price) AS smallest_price, MAX(price) AS largest_price FROM BOOK
""",
    'active_loans': """
SELECT l.loan_id, b.title, m.name AS member, l.loan_date
FROM LOAN l JOIN BOOK b ON l.book_id=b.book_id JOIN MEMBER m ON l.member_id=m.member_id
WHERE l.return_date IS NULL ORDER BY l.loan_date, l.loan_id
""",
    'no_members': """
SELECT m.member_id, m.name, m.email FROM MEMBER m LEFT JOIN LOAN l ON m.member_id=l.member_id
WHERE l.loan_id IS NULL ORDER BY m.member_id
""",
    'no_books': """
SELECT b.book_id, b.title FROM BOOK b LEFT JOIN LOAN l ON b.book_id=l.book_id
WHERE l.loan_id IS NULL ORDER BY b.book_id
""",
    'top_books': """
SELECT b.book_id, b.title, COUNT(l.loan_id) AS loans FROM BOOK b JOIN LOAN l ON b.book_id=l.book_id
GROUP BY b.book_id, b.title ORDER BY loans DESC, b.book_id LIMIT 3
""",
    'top_member': """
SELECT m.member_id, m.name, COUNT(l.loan_id) AS loans FROM MEMBER m JOIN LOAN l ON m.member_id=l.member_id
GROUP BY m.member_id, m.name ORDER BY loans DESC, m.member_id LIMIT 1
""",
    'authors': """
SELECT a.author_id, a.name AS author, COUNT(b.book_id) AS books FROM AUTHOR a LEFT JOIN BOOK b ON a.author_id=b.author_id
GROUP BY a.author_id, a.name ORDER BY a.author_id
""",
    'same_country': """
SELECT b.title, a.name AS author, p.name AS publisher, a.country
FROM BOOK b JOIN AUTHOR a ON b.author_id=a.author_id JOIN PUBLISHER p ON b.publisher_id=p.publisher_id
WHERE a.country=p.country ORDER BY b.book_id
""",
}
