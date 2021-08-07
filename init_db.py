#!/usr/bin/env python3
# coding=UTF-8

import psycopg2

connection = psycopg2.connect(
    database="docker",
    user="docker",
    password="docker",
    host="localhost",
    port="5432",
)

# We need cursor for execution of SQL queries
cursor = connection.cursor()
try:
    with open('sql/schema.sql') as f:
        cursor.execute(f.read())
except psycopg2.errors.DuplicateTable:
    connection.close()
    print("DB already init.")
    pass

connection = psycopg2.connect(
    database="docker",
    user="docker",
    password="docker",
    host="localhost",
    port="5432",
)

# We need cursor for execution of SQL queries
cursor = connection.cursor()

# cursor.execute('SELECT * FROM "People";')
# results = cursor.fetchall()
# print(results)

# character = conn.execute('SELECT * FROM PEOPLE WHERE ID = ?',
#                          (character_id,)).fetchone()
# conn.close()
# if character is None:
#     abort(404)
# return character

connection.commit()
connection.close()
