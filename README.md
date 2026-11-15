# The Reading Room — Lab 4, Part II
**Jana Bassem — 2304066**  
**Farida Mohamed — 2304245**

An extension of our Lab 2 and Lab 3 Flask website, with the same simple interface. All F2.1–F2.6 features and the placeholder bonus are included. Part I is not included. The handout specifies a group of three; add your third teammate's details before submission.

## Start the website
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r website/requirements.txt
```
Copy website/.env.example to website/.env and enter your own MySQL credentials. Use DB_NAME=library_lab4_2304066 and LAB2_DB_NAME=registration. Never publish .env, session files or existing personal data.

On a **fresh machine only**, create and seed Lab 4:
```sh
mysql -u root -p < problem2_DDL.sql
mysql -u root -p < problem2_DML.sql
```
The DDL resets library_lab4_2304066. Do not rerun it on your working database if you want to keep your changes. It does not reset Lab 2 or Lab 3.

If you already have Lab 3 and Lab 4 does not exist, run `python prepare_local.py` instead of those two commands to preserve your old library rows. This refuses to overwrite an existing Lab 4 database. Jana's local database has already been prepared; just start the server.

For Lab 2, keep the existing registration database. On a new machine ONLY, use website/lab2/database/schema.sql to create it; that original script resets registration, so never run it over accounts/tasks you want to keep.

```sh
python website/app.py
```
Open http://127.0.0.1:5003/ . Lab 2 is /lab2/, original library forms are /library/, and Lab 4 is /lab4/. Lab 4 discussion notes are /lab4/discussion.

## DBeaver
Connect to the same host, port, user and password as website/.env (normally 127.0.0.1:3306). Refresh the connection and expand library_lab4_2304066 → Tables. The six tables are AUTHOR, PUBLISHER, CATEGORY, BOOK, MEMBER and LOAN. Open problem2_Queries.sql in an SQL editor and execute the script. It starts with USE library_lab4_2304066 and contains runnable sample values for the search.
Refresh table data after website changes. Commit DBeaver changes if manual commit is enabled, then refresh the website. Do not execute the reset DDL merely to refresh the display.

## Requirements
| Feature | URL | SQL |
|---|---|---|
| F2.1 Search + placeholder bonus | /lab4/search | LIKE, BETWEEN, WHERE, ORDER BY; parameter tuple |
| F2.2 Catalogue | /lab4/catalogue | JOIN four tables |
| F2.3 Reports | /lab4/reports | GROUP BY, HAVING, COUNT, AVG, SUM, MIN, MAX |
| F2.4 Loans | /lab4/loans | JOIN, LEFT JOIN, IS NULL |
| F2.5 Most borrowed | /lab4/popular | GROUP BY, ORDER BY, LIMIT |
| F2.6 Authors | /lab4/authors | LEFT JOIN counts and same-country JOIN |

The DML has 4 authors, 3 publishers, 3 categories, 10 books, 5 members and 12 loans, covering all required edge cases. Local imported Lab 3 records add to these counts. Imported books have unknown publisher/category labels and NULL years until you edit them. Images remain local files. The updated book form includes publisher, category and publication year.

## Files for submission
- problem2_DDL.sql: clean six-table schema with foreign keys and cascading deletes.
- problem2_DML.sql: repeatable demonstration seed for a fresh schema.
- problem2_Queries.sql: every F2 query, labelled, runnable in MySQL/DBeaver.
- website/: Flask site including earlier labs and new pages.
- DISCUSSION_LAB4.md: explanations, expected seed results and practice questions.
- README.md: setup instructions.

lab3-reference/ preserves the old Lab 3 SQL and README for reference, not Lab 4 setup. prepare_local.py imports existing records into a new database. check_lab4.py verifies the SQL and website against a disposable database, requiring CREATE/DROP DATABASE privileges. It never writes to the user's library or registration tables.

## Verification
```sh
python check_lab4.py
```
Checks cover seed counts, reports, all pages, combined search filters, injection-style search text, invalid inputs, book add/edit/delete and cascading deletion. Test data is isolated in lab4_verification_2304066 and removed afterwards.

## Discussion
Read DISCUSSION_LAB4.md or open /lab4/discussion. The source query definitions are website/lab4_queries.py; page handlers are website/lab4.py. MySQL stores data; DBeaver and Flask both access it. Lab 2 retains its own database and login session. DispatcherMiddleware routes /lab2 requests; Flask Blueprints handle the library and reports.

## Part I — COMPANY database questions and answers

These answers use the COMPANY schema from the Lab 4 handout. In Q1.1–Q1.4, replace the example IDs, names, and city with values from your own seed data. The examples assume department 5 exists and department 999 does not. Actual result rows depend on the seed data.

### Q1.1 — INSERT

**Question.** How do you add and display an employee and a project in an existing department? What happens when the employee's department does not exist?

```sql
INSERT INTO employee (ssn, fname, lname, bdate, address, gender, salary, super_ssn, Dno)
VALUES ('900000001', 'Mona', 'Ali', '2000-04-15', 'Alexandria', 'F', 4500, NULL, 5);

INSERT INTO project (Pnumber, Pname, Plocation, Dno)
VALUES (90, 'Training', 'Alexandria', 5);

SELECT * FROM employee WHERE ssn = '900000001';
SELECT * FROM project WHERE Pnumber = 90;

-- Run separately to observe the expected error.
INSERT INTO employee (ssn, fname, lname, bdate, address, gender, salary, super_ssn, Dno)
VALUES ('900000002', 'Nour', 'Ali', '2000-05-15', 'Alexandria', 'F', 4500, NULL, 999);
```

The first two statements add one row each. The final insert is rejected because `employee.Dno` must reference an existing department (MySQL foreign key error 1452).

### Q1.2 — UPDATE

**Question.** How do you give employees in one department a 10% raise, change a project's location, and check what happens if you assign an employee to a missing department?

```sql
UPDATE employee SET salary = salary * 1.10 WHERE Dno = 5;
SELECT ssn, fname, lname, salary FROM employee WHERE Dno = 5;

UPDATE project SET Plocation = 'Cairo' WHERE Pnumber = 90;
SELECT Pnumber, Pname, Plocation FROM project WHERE Pnumber = 90;

-- Run separately to observe the expected error.
UPDATE employee SET Dno = 999 WHERE ssn = '900000001';
```

A salary of 4500 becomes 4950. The project's location becomes Cairo. MySQL rejects the last update with a foreign key error (1452), so the employee's department stays the same.

### Q1.3 — DELETE and ROLLBACK

**Question.** How do you delete one dependent and one work assignment? Why can a department with employees be blocked from deletion, and what does rolling back an unfiltered delete do?

```sql
DELETE FROM dependent WHERE essn = '100000001' AND dependent_name = 'Sara';
DELETE FROM works_on WHERE essn = '100000001' AND Pno = 1;

-- Run separately to observe the expected error with restrictive foreign keys.
DELETE FROM department WHERE Dnumber = 5;

START TRANSACTION;
DELETE FROM dependent;
SELECT * FROM dependent;
ROLLBACK;
SELECT * FROM dependent;
```

Each targeted delete uses both columns of the row's composite key. With restrictive foreign keys, MySQL rejects the department deletion (error 1451) while employees or projects reference it. Reassign those employees and projects to valid departments first, then delete the department. If you intend to delete the employees and projects too, clear their dependent and work assignment rows and resolve any supervisor or manager references before deleting the referenced rows.

On an InnoDB table, the unfiltered delete removes every dependent row inside the transaction, so the first SELECT returns no rows. ROLLBACK restores the rows that existed when the transaction started. The earlier targeted deletes are outside that transaction and are not reversed if they were already committed.

### Q1.4 — WHERE and DISTINCT

**Question.** Find employees earning 3000–6000 in a given city, find employees with no supervisor, and list each staffed department number once.

```sql
SELECT fname, lname, salary
FROM employee
WHERE salary BETWEEN 3000 AND 6000 AND address LIKE '%Alexandria%'
ORDER BY salary DESC;

SELECT ssn, fname, lname FROM employee WHERE super_ssn IS NULL;

SELECT DISTINCT Dno FROM employee WHERE Dno IS NOT NULL;
```

BETWEEN includes both endpoints. IS NULL checks for a missing supervisor, and DISTINCT removes repeated department numbers.

### Q1.5 — Aggregation

**Question.** How do you get the employee count and the total, average, minimum, and maximum salary in one query?

```sql
SELECT COUNT(*) AS employee_count, SUM(salary) AS total_salary,
       AVG(salary) AS average_salary, MIN(salary) AS minimum_salary,
       MAX(salary) AS maximum_salary
FROM employee;
```

The query returns one summary row. COUNT(*) counts all employees, while the salary aggregates ignore NULL salaries.

### Q1.6 — GROUP BY

**Question.** How do you show the employee count and average salary for each department number?

```sql
SELECT Dno, COUNT(*) AS employee_count, AVG(salary) AS average_salary
FROM employee
GROUP BY Dno;
```

Each distinct Dno in the employee table produces one result row. Departments with zero employees appear in Q1.10 instead.

### Q1.7 — HAVING

**Question.** Which departments have more than two employees, first counting everyone and then counting only employees earning above 3000?

```sql
SELECT Dno, COUNT(*) AS employee_count
FROM employee
WHERE Dno IS NOT NULL
GROUP BY Dno
HAVING COUNT(*) > 2;

SELECT Dno, COUNT(*) AS employee_count
FROM employee
WHERE Dno IS NOT NULL AND salary > 3000
GROUP BY Dno
HAVING COUNT(*) > 2;
```

WHERE filters individual rows before grouping, while HAVING filters the groups after their counts have been calculated.

### Q1.8 — JOIN

**Question.** How do you show each employee's first and last names with their department name?

```sql
SELECT e.fname, e.lname, d.Dname
FROM employee e
JOIN department d ON e.Dno = d.Dnumber;
```

The join replaces the department ID in the displayed result with the matching department name.

### Q1.9 — JOIN three tables

**Question.** For each work assignment, how do you show the employee's last name, project name, and hours?

```sql
SELECT e.lname, p.Pname, w.hours
FROM works_on w
JOIN employee e ON w.essn = e.ssn
JOIN project p ON w.Pno = p.Pnumber;
```

WORKS_ON connects each employee to a project and stores the hours for that assignment.

### Q1.10 — LEFT JOIN

**Question.** How do you count employees in every department, including empty ones, and find projects with no work assignments?

```sql
SELECT d.Dnumber, d.Dname, COUNT(e.ssn) AS employee_count
FROM department d
LEFT JOIN employee e ON e.Dno = d.Dnumber
GROUP BY d.Dnumber, d.Dname;

SELECT p.Pnumber, p.Pname
FROM project p
LEFT JOIN works_on w ON w.Pno = p.Pnumber
WHERE w.Pno IS NULL;
```

COUNT(e.ssn) gives zero for a department without a match because it ignores NULL. The second query selects projects whose right-hand work assignment is missing.

### Q1.11 — Self join

**Question.** How do you show every employee with their supervisor's name?

```sql
SELECT e.fname, e.lname, s.fname AS supervisor_fname, s.lname AS supervisor_lname
FROM employee e
LEFT JOIN employee s ON e.super_ssn = s.ssn;
```

Both aliases refer to EMPLOYEE. The left join keeps employees without supervisors, with NULL in the supervisor name columns.

### Q1.12 — JOIN, GROUP BY, and HAVING

**Question.** Which projects have more than 20 total work hours, ordered from the highest total down?

```sql
SELECT p.Pnumber, p.Pname, SUM(w.hours) AS total_hours
FROM project p
JOIN works_on w ON w.Pno = p.Pnumber
GROUP BY p.Pnumber, p.Pname
HAVING SUM(w.hours) > 20
ORDER BY total_hours DESC;
```

The join gets the work assignments for each project. SUM adds their hours, and HAVING excludes totals of 20 or less. Grouping by the project ID keeps different projects with the same name separate.
