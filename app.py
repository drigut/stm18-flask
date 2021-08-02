#!/usr/bin/env python3
# coding=UTF-8

import os
import requests

from flask import Flask, render_template, json, send_from_directory
from flask_bootstrap import Bootstrap

PEOPLE = 'https://swapi.dev/api/people/'

app = Flask(__name__)
Bootstrap(app)

# TODO: Make connector to psql and write info to DB
# def post_to_db():
#     return pass


def get_item(req):
    jsonData = json.dumps(requests.get(req).json())
    return json.loads(jsonData)


def get_characters():
    characters = list()
    count = get_item(PEOPLE)["count"]

    while count > 0:
        try:
            characters.append(dict(
                name=get_item(PEOPLE + str(count))["name"],
                gender=get_item(PEOPLE + str(count))["gender"],
                homeworld=get_item(get_item(PEOPLE + str(count))["homeworld"])["name"],
                starships=[{'name': get_item(item)["name"],
                            'model': get_item(item)["model"],
                            'manufacturer': get_item(item)["manufacturer"],
                            'cargo_capacity': get_item(item)["cargo_capacity"]}
                           for item in get_item(PEOPLE + str(count))["starships"]]))

            count -= 1

        except KeyError:
            count -= 1
            pass

    return characters


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error():
    return render_template('500.html'), 500


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/people', methods=['GET'])
def get_people():
    print(get_characters())
    return 'Done!'


@app.route('/update-db', methods=['GET', 'POST'])
def update_db():
    return 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
