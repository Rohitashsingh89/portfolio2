import pymysql
conn = pymysql.connect(user='root', password='', host='localhost',database='rohitashsingh')
cursor = conn.cursor()
# query = 'SELECT * FROM CONTACT;'
query = 'SELECT * FROM posts;'
r = cursor.execute(query)
data = cursor.fetchall()
print(data)