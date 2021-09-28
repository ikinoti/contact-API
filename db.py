import pymysql

conn = pymysql.connect(
  host='sql6.freesqldatabase.com',
  database='sql6440738',
  user= 'sql6440738',
  password= 'HUqWVBQGJ6',
  charset='utf8mb4',
  cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

sql_query = '''CREATE TABLE contact (
  id integer PRIMARY KEY AUTO_INCREMENT,
  name text NOT NULL,
  contact text NOT NULL,
  email text NOT NULL,
  location text NOT NULL,
  meetPlace text NOT NULL
)'''

cursor.execute(sql_query)
conn.close()