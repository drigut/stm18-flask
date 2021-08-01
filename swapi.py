#!/usr/bin/env python3
# coding=UTF-8

from flask import Flask, json
import requests

PEOPLE = 'https://swapi.dev/api/people/'

app = Flask(__name__)


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


# TODO: Make connector to psql and write info to DB
def post_to_db():
    return pass


@app.route('/', methods=['GET'])
def hello():
    return 'Hello, Flask!'


@app.route('/people', methods=['GET'])
def get_people():
    print(get_characters())
    return 'Done!'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
