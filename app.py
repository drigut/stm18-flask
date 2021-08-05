#!/usr/bin/env python3
# coding=UTF-8

import os
import sqlite3
from datetime import time

import requests

from flask import Flask, request, render_template, send_from_directory, url_for, flash, redirect, json, Response, \
    jsonify
from flask_bootstrap import Bootstrap
from werkzeug.exceptions import abort

PEOPLE = 'https://swapi.dev/api/people/'
# PLANETS = 'https://swapi.dev/api/planets/'
# STARSHIPS = 'https://swapi.dev/api/starships/'


def get_value(req):
    jsonData = json.dumps(requests.get(req).json())
    return json.loads(jsonData)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
Bootstrap(app)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_character(character_id):
    conn = get_db_connection()
    character = conn.execute('SELECT * FROM PEOPLE WHERE ID = ?',
                             (character_id,)).fetchone()
    conn.close()
    if character is None:
        abort(404)
    return character


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/update')
def update():
    connection = sqlite3.connect('database.db')

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cur = connection.cursor()
    count = get_value(PEOPLE)["count"]

    while count > 0:
        try:
            name = get_value(PEOPLE + str(count))["name"]
            gender = get_value(PEOPLE + str(count))["gender"]
            homeworld = get_value(get_value(PEOPLE + str(count))["homeworld"])["name"]
            starships = [{'name': get_value(item)["name"],
                        'model': get_value(item)["model"],
                        'manufacturer': get_value(item)["manufacturer"],
                        'cargo_capacity': get_value(item)["cargo_capacity"]}
                       for item in get_value(key + str(count))["starships"]]

            cur.execute("INSERT INTO PEOPLE (NAME, GENDER, HOMEWORLD, STARSHIPS) VALUES (?, ?, ?, ?)",
                        (name, gender, homeworld, starships))

            count -= 1

        except KeyError:
            count -= 1
            pass

    connection.commit()
    connection.close()

    return render_template('update.html')


@app.route('/characters')
def characters():
    conn = get_db_connection()
    characters = conn.execute('SELECT * FROM PEOPLE').fetchall()
    conn.close()
    return render_template('characters.html', characters=characters)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        homeworld = request.form['homeworld']

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO PEOPLE (NAME, GENDER, HOMEWORLD) VALUES (?, ?)',
                         (name, gender, homeworld))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    character = get_character(id)

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        homeworld = request.form['homeworld']

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE PEOPLE SET NAME = ?, GENDER = ?, HOMEWORLD = ?'
                         ' WHERE ID = ?',
                         (name, gender, homeworld, id))
            conn.commit()
            conn.close()
            return redirect(url_for('characters'))

    return render_template('edit.html', character=character)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    character = get_character(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM PEOPLE WHERE ID = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(character['name']))
    return redirect(url_for('characters'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
