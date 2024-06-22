This is to create a database from a .sql file, and save it as a database

- to create .sql file from .sqlite
sqlite3 olist.sqlite .dump > ecommerce.sql

- to initialize a database called 'sqldb':
sqlite3 ecommerce.db

- to load ecommer.sql into ecommerce.db
.read ecommerce.sql

- to run any query
Example:
SELECT * FROM orders LIMIT 10;