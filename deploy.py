import requests
from bs4 import BeautifulSoup
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True
session = requests.session()

r = session.get('https://www.worldometers.info/coronavirus/')
soup = BeautifulSoup(r.text, 'html.parser')
table = soup.select_one('table').select_one('tbody')
store = []

for tr in table.select('tr'):
    country = {'Name': tr.select('td')[0].text.strip(), 'Total': tr.select('td')[1].text.strip(),
               'New': tr.select('td')[2].text.strip(), 'Death': tr.select('td')[3].text.strip(),
               'NewDeath': tr.select('td')[4].text.strip(), 'Recovered': tr.select('td')[5].text.strip(),
               'Active': tr.select('td')[6].text.strip(), 'Serious': tr.select('td')[7].text.strip()}
    store.append(country)


@app.route('/', methods=['GET'])
def api_all():
    return '<h1>hello</h1>'


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/countries/all', methods=['GET'])
def api_all():
    return jsonify(store)
