
from flask import Flask, request, jsonify
import json
import pymysql

app = Flask(__name__)

def db_connection():
  conn = None
  try:
    conn = pymysql.connect(
      host='sql6.freesqldatabase.com',
      database='sql6440738',
      user= 'sql6440738',
      password= 'HUqWVBQGJ6',
      charset='utf8mb4',
      cursorclass=pymysql.cursors.DictCursor
    )
  except pymysql.Error as e:
    print(e)
  return conn

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
  conn = db_connection()
  cursor = conn.cursor()

  if request.method == 'GET':
    cursor.execute('SELECT* FROM contact')
    contacts = [
      dict(id=row['id'], name=row['name'], contact=row['contact'], email=row['email'], location=row['location'], meetPlace=row['meetPlace'])
      for row in cursor.fetchall()
    ]
    if contacts is not None:
      return jsonify(contacts)

  if request.method =='POST':
    new_name = request.form['name']
    new_contact = request.form['contact']
    new_email = request.form['email']
    new_location = request.form['location']
    new_meetPlace = request.form['meetPlace']
    
    sql = '''INSERT INTO contact (name, contact, email, location, meetPlace) VALUES (%s, %s, %s, %s, %s)'''
    cursor = cursor.execute(sql, (new_name, new_contact, new_email, new_location, new_meetPlace))
    conn.commit()

    return f'Contact with the id: %s created successfully', 201

@app.route('/contact/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_contact(id):
  conn = db_connection()
  cursor = conn.cursor()
  contact = None

  if request.method == 'GET':
    cursor.execute('SELECT * FROM contact WHERE id=%s', (id,))
    rows = cursor.fetchall()
    for r in rows:
      contact=r
    if contact is not None:
      return jsonify(contact),200
    else:
      return 'Something wrong',404

  if request.method == 'PUT':
    sql = '''UPDATE contact
            SET name=%s,
                contact=%s,
                email=%s,
                location=%s,
                meetPlace=%s
            WHERE id=%s'''

    name = request.form['name']
    contact = request.form['contact']
    email = request.form['email']
    location = request.form['location']
    meetPlace = request.form['meetPlace']
    updated_contact = {
      'id': id,
      'name':name,
      'contact':contact,
      'email':email,
      'location':location,
      'meetPlace':meetPlace
    }
    cursor.execute(sql, (name,contact,email,location,meetPlace, id))
    conn.commit()

    return jsonify(updated_contact)
  
  if request.method == 'DELETE':
    sql='''DELETE FROM contact WHERE id=%s '''
    cursor.execute(sql,(id,))
    conn.commit()
    return 'The contact with id: {} has been deleted.'.format(id),200


if __name__ == '__main__':
  app.run(debug = True)