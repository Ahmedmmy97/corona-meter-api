import requests
from bs4 import BeautifulSoup
from flask import request, jsonify, Flask

app = Flask(__name__)


def scrapData():
    session = requests.session()

    r = session.get('https://www.worldometers.info/coronavirus/')
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.select_one('table').select_one('tbody')
    store = []

    for tr in table.select('tr'):
        country = {'Name': tr.select('td')[1].text.strip(), 'Total': tr.select('td')[2].text.strip(),
                   'New': tr.select('td')[3].text.strip(), 'Death': tr.select('td')[4].text.strip(),
                   'NewDeath': tr.select('td')[5].text.strip(), 'Recovered': tr.select('td')[6].text.strip(),
                   'Active': tr.select('td')[7].text.strip(), 'Serious': tr.select('td')[8].text.strip()}
        store.append(country)
        sortedStore = sorted(store, key=lambda i: int(i['Total'].replace(',', '')), reverse=True)
    return sortedStore


@app.route('/')
def index():
    return '<div><h1>Welcome To Corona Meter Api</h1><Span>Developed by Ahmed Yousef<span></div>'


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/countries/all', methods=['GET'])
def api_all():
    return jsonify(scrapData())


