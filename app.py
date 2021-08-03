#!/usr/bin/env python3
# coding=UTF-8

import os
import sqlite3

from flask import Flask, request, render_template, send_from_directory, url_for, flash, redirect
from flask_bootstrap import Bootstrap
from werkzeug.exceptions import abort

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
    conn = get_db_connection()
    characters = conn.execute('SELECT * FROM PEOPLE').fetchall()
    conn.close()
    return render_template('index.html', characters=characters)


@app.route('/<int:character_id>')
def character(character_id):
    character = get_character(character_id)
    return render_template('character.html', character=character)


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
            return redirect(url_for('index'))

    return render_template('edit.html', character=character)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    character = get_character(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM PEOPLE WHERE ID = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(character['name']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
