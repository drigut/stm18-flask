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
cursor.execute('''SELECT * FROM "People";''')
results = cursor.fetchall()
print(results)

connection.commit()
connection.close()
