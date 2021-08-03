#!/usr/bin/env python3
# coding=UTF-8

import sqlite3
import requests
from flask import json

PEOPLE = 'https://swapi.dev/api/people/'
# PLANETS = 'https://swapi.dev/api/planets/'
# STARSHIPS = 'https://swapi.dev/api/starships/'


def get_value(req):
    jsonData = json.dumps(requests.get(req).json())
    return json.loads(jsonData)


def get_character():
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
            # starships = [{'name': get_value(item)["name"],
            #             'model': get_value(item)["model"],
            #             'manufacturer': get_value(item)["manufacturer"],
            #             'cargo_capacity': get_value(item)["cargo_capacity"]}
            #            for item in get_value(key + str(count))["starships"]])

            cur.execute("INSERT INTO PEOPLE (NAME, GENDER, HOMEWORLD) VALUES (?, ?, ?)",
                        (name, gender, homeworld))

            count -= 1

        except KeyError:
            count -= 1
            pass

    connection.commit()
    connection.close()


if __name__ == '__main__':
    get_character()
