import pymysql
connection=pymysql.connect(host='', database='', user='', password='')
cursor = connection.cursor()
cursor.execute('''SELECT count(*) FROM ut_cas4.SERVICETICKET;''')
result = cursor.fetchall()
print(int(result[0][0]))
