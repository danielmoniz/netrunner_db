import sqlite3

connection = sqlite3.connect("cards.db")
c = connection.cursor()

query_string = "SELECT name FROM corp WHERE rating = ? AND identity LIKE '%Weyland%' ORDER BY name"
select_all = c.execute(query_string, (5,))

print '='*10
for row in select_all:
    print row[0]
print '='*10

connection.close()
