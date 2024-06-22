import sqlite3

# Connect to sqlite
connection = sqlite3.connect('data/sqldb1.db')

# Create a cursor for CRUD
cursor = connection.cursor()

# Run a query
data = cursor.execute("""SELECT * FROM leads_closed LIMIT 10; """)

for row in data:
    print(row)

# Close connection
connection.commit()
connection.close()