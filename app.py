#!/usr/bin/env python3
# coding=UTF-8

import os
import psycopg2
import requests

from flask import Flask, request, render_template, send_from_directory, url_for, flash, redirect, json
from flask_bootstrap import Bootstrap
from werkzeug.exceptions import abort

PEOPLE = 'https://swapi.dev/api/people/'
STARSHIPS = 'https://swapi.dev/api/starships/'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
Bootstrap(app)


def db_connection():
    connection = psycopg2.connect(
        database="docker",
        user="docker",
        password="docker",
        host="localhost",
        port="5432",
    )
    print("DB connected.")
    return connection


# TODO: fix DB init
def db_init():
    cursor = db_connection().cursor()
    try:
        with open('sql/schema.sql') as f:
            cursor.execute(f.read())
            db_connection().commit()
            db_connection().close()
            status = "DB successfully initialize."
    except psycopg2.errors.DuplicateTable:
        db_connection().close()
        status = "DB already initialized."
        pass
    return status


def get_character(character_id):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM STARSHIPS WHERE ID = %s', (character_id,))
    character = cursor.fetchone()
    connection.close()
    if character is None:
        abort(404)
    return character


def get_value(req):
    jsonData = json.dumps(requests.get(req).json())
    return json.loads(jsonData)


def get_people(cursor, connection):
    count = 100

    while count > 0:
        try:
            if len(get_value(PEOPLE + str(count))["starships"]) != 0:
                name = get_value(PEOPLE + str(count))["name"]
                gender = get_value(PEOPLE + str(count))["gender"]
                homeworld = get_value(get_value(PEOPLE + str(count))["homeworld"])["name"]

                cursor.execute('INSERT INTO PEOPLE (NAME, GENDER, HOMEWORLD)'
                               'VALUES (%s, %s, %s)', (name, gender, homeworld))
            else:
                pass

            count -= 1

        except KeyError:
            count -= 1
            pass

        except psycopg2.errors.UniqueViolation:
            connection.rollback()
            count -= 1
            pass


def get_starships(cursor, connection):
    count = 100

    while count > 0:
        try:
            if len(get_value(STARSHIPS + str(count))["pilots"]) != 0:
                for item in get_value(STARSHIPS + str(count))["pilots"]:
                    name = get_value(STARSHIPS + str(count))["name"]
                    model = get_value(STARSHIPS + str(count))["model"]
                    manufacturer = get_value(STARSHIPS + str(count))["manufacturer"]
                    lading = get_value(STARSHIPS + str(count))["cargo_capacity"]
                    lading = 0 if lading == "unknown" else lading
                    pilot = get_value(item)["name"]

                    cursor.execute('INSERT INTO STARSHIPS (NAME, MODEL, MANUFACTURER, LADING, PILOT)'
                                   'VALUES (%s, %s, %s, %s, %s)', (name, model, manufacturer, lading, pilot))
            else:
                name = get_value(STARSHIPS + str(count))["name"]
                model = get_value(STARSHIPS + str(count))["model"]
                manufacturer = get_value(STARSHIPS + str(count))["manufacturer"]
                lading = get_value(STARSHIPS + str(count))["cargo_capacity"]
                lading = 0 if lading == "unknown" else lading
                pilot = "n/a"

                cursor.execute('INSERT INTO STARSHIPS (NAME, MODEL, MANUFACTURER, LADING, PILOT)'
                               'VALUES (%s, %s, %s, %s, %s)', (name, model, manufacturer, lading, pilot))

            count -= 1

        except KeyError:
            count -= 1
            pass

        except psycopg2.errors.UniqueViolation:
            connection.rollback()
            count -= 1
            pass


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update')
def update():
    connection = db_connection()
    cursor = connection.cursor()
    get_people(cursor, connection)
    get_starships(cursor, connection)
    connection.commit()
    connection.close()
    return render_template('update.html')


@app.route('/characters')
def characters():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM STARSHIPS')
    characters = cursor.fetchall()
    connection.close()
    return render_template('characters.html', characters=characters)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        homeworld = request.form['homeworld']
        starships = request.form['starships']

        if not name:
            flash('Name is required!')
        else:
            connection = db_connection()
            connection.execute('INSERT INTO PEOPLE (NAME, GENDER, HOMEWORLD, STARSHIPS) VALUES (%s, %s, %s, %s)',
                               (name, gender, homeworld, starships))
            connection.commit()
            connection.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    character = get_character(id)

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        homeworld = request.form['homeworld']
        print(name, gender)

        if not name:
            flash('Name is required!')
        else:
            connection = db_connection()
            cursor = connection.cursor()
            cursor.execute('UPDATE PEOPLE SET NAME = %s, GENDER = %s, HOMEWORLD = %s WHERE ID = %s',
                           (name, gender, homeworld, id))
            connection.commit()
            connection.close()
            return redirect(url_for('characters'))

    return render_template('edit.html', character=character)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    character = get_character(id)
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM PEOPLE WHERE ID = %s', (id,))
    connection.commit()
    connection.close()
    flash('"{}" was successfully deleted!'.format(character[1]))
    return redirect(url_for('characters'))


if __name__ == '__main__':
    db_init()
    app.run(debug=True, port=5000)
