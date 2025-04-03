import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'elite102', password = 'g0SUHUg0')

cursor = connection.cursor()

testQuery = ("SELECT * FROM test")

cursor.execute(testQuery)

for item in cursor:
    print(item)

cursor.close()

connection.close()