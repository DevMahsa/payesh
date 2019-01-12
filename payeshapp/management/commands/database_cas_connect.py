import pymysql
connection=pymysql.connect(host='127.0.0.1',database='zabbix',user='zabbix',password='root')
cursor = connection.cursor()
cursor.execute('''SELECT count(itemid) AS history FROM history WHERE itemid NOT IN (SELECT itemid FROM items WHERE status='0');
''')
result = cursor.fetchall()
