# Lab 4 discussion guide
Jana Bassem — 2304066 | Farida Mohamed — 2304245

## What changed since Lab 3?
Lab 3 had AUTHOR and BOOK. Lab 4 adds PUBLISHER, CATEGORY, MEMBER and LOAN, and adds publish_year, publisher_id and category_id to BOOK. The original add/edit/delete and image forms remain. Lab 2 still uses registration for accounts and tasks. The library now uses library_lab4_2304066.

## Explain the relationships
AUTHOR → BOOK, PUBLISHER → BOOK and CATEGORY → BOOK are one-to-many. MEMBER → LOAN and BOOK → LOAN are one-to-many. LOAN records the many-to-many relationship between members and books over time. A primary key identifies a row; a foreign key requires a referenced parent. return_date IS NULL means an outstanding loan.
Deleting an author cascades to their books, then those books' loans. Deleting a publisher, category or member with referenced rows is restricted by the default foreign-key behaviour. Demonstrate deletion only in a disposable copy.

## F2.1: Search and the bonus
WHERE combines title, price and category filters with AND. LIKE '%Palace%' matches a title containing Palace. BETWEEN includes both boundaries. ORDER BY price ASC puts the cheapest first. A blank category means all categories. Blank price limits use 0 and 99999999.99. Invalid prices or reversed limits show a validation message.
The Python search() function validates inputs then calls rows(SEARCH, parameters). cursor.execute(sql, parameters) passes values separately through PyMySQL placeholders (%s); user input is never concatenated into SQL. This is the handout's prepared-statement/placeholder bonus. PyMySQL parameter binding safely escapes values; it is not a server-side PREPARE statement. SQL keywords inside a user's search remain data. Percent and underscore remain LIKE pattern wildcards.
Try Palace, minimum 15, maximum 20, Fiction: the demonstration data returns Palace Walk at 18.50. Try an apostrophe: it must not cause a SQL error.

## F2.2: Catalogue
JOIN pairs each book with its author, publisher and category using the corresponding foreign key and primary key. We show names rather than asking the reader to interpret IDs. An INNER JOIN returns matching rows. The mandatory publisher/category fields keep new books visible in the catalogue.

## F2.3: Reports
GROUP BY category gives one result per category. COUNT(b.book_id) counts books; AVG(b.price) gives their average price. LEFT JOIN also keeps empty categories, where count is 0 and average is NULL (shown as a dash). Never use COUNT(*) for the zero-book count: the unmatched parent row would be counted as 1.
HAVING COUNT(b.book_id)>=2 filters author groups AFTER counting. WHERE filters individual rows BEFORE grouping. SUM, MIN and MAX without GROUP BY summarise the whole BOOK table. The fresh ten-book seed has total 199.50, minimum 12.00 and maximum 30.00. Your imported Lab 3 books increase the live total to 254.25.
Group by both ID and name: different people can share a name. Every selected nonaggregate column is included in GROUP BY.

## F2.4: Loans
JOIN LOAN to BOOK and MEMBER to display titles and names. WHERE return_date IS NULL selects unreturned loans; '= NULL' does not work as a NULL test.
LEFT JOIN keeps every member/book even without loans. WHERE l.loan_id IS NULL finds no matching loan. This is different from return_date IS NULL: one means never borrowed, the other means borrowed but not returned. Fresh seed has four outstanding loans, one member without loans and four books never borrowed.

## F2.5: Most borrowed
COUNT(l.loan_id) counts all historical loan records, including returned ones. GROUP BY book/member, ORDER BY loans DESC and LIMIT 3 or LIMIT 1 produce rankings. IDs provide deterministic tie-breaking. Seed results: Palace Walk 4, Palace of Desire 3, Sugar Street 2; Demo Reader A has 5 loans. This requirement returns exactly three books and one member, not all tied records.

## F2.6: Authors
LEFT JOIN keeps the author with zero books. COUNT(b.book_id) gives zero for that author. The same-country report joins BOOK, AUTHOR and PUBLISHER, then uses WHERE a.country=p.country. This compares country values, not names or IDs.

## Python and the two earlier labs
create_app() registers the library and lab4 Blueprints. /library contains the earlier library forms; /lab4 contains the new searches and reports. DispatcherMiddleware mounts the Lab 2 application at /lab2. Navigation links switch pages; DispatcherMiddleware routes requests, it does not merge databases.
database() opens a PyMySQL connection using private .env settings and closes it in finally. rows() executes a SELECT and fetchall() returns dictionaries to the Jinja template. search() handles filters. report() chooses an allowed report. book_form() validates and saves all seven book fields. connection.commit() saves INSERT/UPDATE/DELETE; SELECT needs no commit to save results.
HTML structures the pages, CSS styles them, JavaScript keeps the existing theme/image interactions, Python/Flask handles requests, and MySQL executes SQL. DBeaver is another client of the same MySQL database, not the database itself.

## Demonstration sequence
1. Open / and show all three lab links; visit Lab 2 and verify your existing login/tasks.
2. Open /library and show the imported books and old image support.
3. Open /lab4 and demonstrate the Palace search and an empty result.
4. Visit every report and explain its SQL using problem2_Queries.sql.
5. In DBeaver, select library_lab4_2304066, refresh its Tables node, and show all six tables. Run SELECT DATABASE(); and SELECT * FROM BOOK;.
6. Add or edit a book in the website, refresh DBeaver's BOOK data, and verify the same values. Refresh the web page after editing in DBeaver, and commit DBeaver edits if manual commit is enabled.
7. Show the parameter tuple in search() for the bonus.

## Questions to practise
Why LEFT JOIN instead of JOIN for authors? To retain authors without books.
Why COUNT(book_id) instead of COUNT(*)? To avoid counting the unmatched parent row.
Why HAVING? It filters grouped aggregate results.
What does BETWEEN mean? Both limits are included.
What is a foreign key? A reference that enforces parent-child consistency.
What happens when an author is deleted? Their books and those books' loans cascade away.
Why placeholders? They keep user values separate from SQL syntax.
Why can website and DBeaver differ? Different schemas, cached results or uncommitted edits.

## Data preservation
The local setup copied three authors and four books from Lab 3 without changing their IDs, names, prices or authors. Unknown old publication years remain NULL; publisher/category are explicitly labelled imported/unknown. The original Lab 3 database and project remain intact. Lab 2 is still connected to the same registration database. Lab 3 and Lab 4 library databases are separate snapshots: later changes to one do not automatically update the other.
