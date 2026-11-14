"""One-time non-destructive copy of Lab 3 records into the NEW Lab 4 database.
Refuses to overwrite any existing Lab 4 database. Lab 2 and Lab 3 are read-only.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / 'website'))
from app import app
import pymysql

root = Path(__file__).parent
config = app.config
connection = pymysql.connect(host=config['DB_HOST'], port=config['DB_PORT'], user=config['DB_USER'],
                             password=config['DB_PASSWORD'], charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
with connection, connection.cursor() as cursor:
    cursor.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME='library_lab4_2304066'")
    if cursor.fetchone():
        raise SystemExit('Lab 4 already exists; refusing to overwrite it.')
    cursor.execute('SELECT * FROM library_lab3_2304066.AUTHOR'); authors = cursor.fetchall()
    cursor.execute('SELECT * FROM library_lab3_2304066.BOOK'); books = cursor.fetchall()
    if any(x['author_id']>=4001 for x in authors) or any(x['book_id']>=4001 for x in books):
        raise SystemExit('Existing IDs overlap demonstration range; review before importing.')
    for file in ['problem2_DDL.sql','problem2_DML.sql']:
        content='\n'.join(line for line in (root/file).read_text().splitlines() if not line.lstrip().startswith('--'))
        for statement in content.split(';'):
            if statement.strip() and not statement.strip().startswith('DROP DATABASE'):
                cursor.execute(statement)
    # Explicitly mark unknown historical metadata; never invent publication details.
    cursor.execute("INSERT INTO PUBLISHER VALUES (1,'Unknown — imported from Lab 3','Unknown')")
    cursor.execute("INSERT INTO CATEGORY VALUES (1,'Uncategorised — imported from Lab 3')")
    for a in authors:
        cursor.execute('INSERT INTO AUTHOR VALUES (%s,%s,%s)',(a['author_id'],a['name'],a['country']))
    for b in books:
        cursor.execute('INSERT INTO BOOK VALUES (%s,%s,%s,NULL,%s,1,1)',(b['book_id'],b['title'],b['price'],b['author_id']))
    connection.commit()
    print(f'Preserved {len(authors)} authors and {len(books)} books; added Lab 4 demonstration data. Lab 2 and Lab 3 unchanged.')
