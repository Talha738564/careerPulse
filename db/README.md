# Oracle academic package
Run schema.sql, seed_data.sql, then views.sql in a new Oracle 19c+ course schema.
queries.sql contains bound discovery, matching, aggregation, subquery, deadline,
analytics and notification demonstrations. transactions.sql shows atomic writes.
See ../docs/DATABASE_DESIGN.md and ../docs/screenshots/oracle-erd.png for the full
ERD, normalization argument, installation sequence and live acceptance checklist.

No Oracle instance is configured. These scripts have been syntax-parsed, not
executed on Oracle. The web app remains explicitly memory-backed. oracle_gateway.py
contains optional query/transaction examples and a read-only connection check;
it is not a full application persistence adapter. Never use a SQLite substitute.
