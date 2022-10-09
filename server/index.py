import requests
from flask import Flask, request

from utils.catch_errors import catch_errors
from utils.helpers import simplify_url
from utils.propagating_thread import PropagatingThread

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Hello World 🍕'

@app.route('/search', methods=['GET'])
@catch_errors
def search():
    query = request.args.get('q')
    search_body = '{"query":"%s"}' % query
    query_result = requests.get(
        f'https://apis.justwatch.com/content/titles/pt_BR/popular?language=en&body={search_body}'
    ).json()

    return query_result['items']

@app.route('/offers/<content_type>/<content_id>', methods=['GET'])
@catch_errors
def offers(content_type, content_id):
    preffered_currency = request.args.get('currency', 'NOK')

    rates = requests.get(
        'https://currency.djupvik.dev/rates'
    ).json()

    def convert(price, from_curr, to_curr):
        return price * rates[to_curr] / rates[from_curr]

    locales = requests.get(
        'http://apis.justwatch.com/content/locales/state'
    ).json()
    locales = [(locale['full_locale'], locale['country']) for locale in locales]

    def extract_service_url(offer):
        return simplify_url(list(offer['urls'].values())[0])


    def extract_offers(offers, list, location):
        if rates is None:
            return

        for offer in offers:
            if 'retail_price' not in offer:
                continue
            price = offer['retail_price']
            currency = offer['currency']


            price = convert(price, currency, preffered_currency)

            list.append((price, extract_service_url(offer), location))


    streaming_services_data = {}
    renting_offers_data = []
    buying_offers_data = []


    def fetch_and_extract_offers(locale, location):
        offers = requests.get(
            f'http://apis.justwatch.com/content/titles/{content_type}/{content_id}/locale/{locale}'
        ).json()

        if 'offers' not in offers:
            return

        offers = offers['offers']
        offers = [(offer, offer['monetization_type']) for offer in offers]

        streaming_services = [extract_service_url(
            offer) for offer, type in offers if type == 'flatrate']
        renting_offers = [offer for offer, type in offers if type == 'rent']
        buying_offers = [offer for offer, type in offers if type == 'buy']

        for streaming_service in streaming_services:
            if streaming_service not in streaming_services_data:
                streaming_services_data[streaming_service] = [location]
            elif location not in streaming_services_data[streaming_service]:
                streaming_services_data[streaming_service].append(location)

        extract_offers(renting_offers, renting_offers_data, location)
        extract_offers(buying_offers, buying_offers_data, location)


    threads = []
    for locale, location in locales:
        t = PropagatingThread(target=lambda: fetch_and_extract_offers(locale, location))
        threads.append(t)
        t.deamon = True
        t.start()

    for t in threads:
        t.join()
        
    renting_offers_data = list(dict.fromkeys(renting_offers_data))
    renting_offers_data.sort(key=lambda offer: offer[0])
    renting_offers_data = [{
            'price': p,
            'url': u,
            'location': l,
        } for p, u, l in renting_offers_data]

    buying_offers_data = list(dict.fromkeys(buying_offers_data))
    buying_offers_data.sort(key=lambda offer: offer[0])
    buying_offers_data = [{
        'price': p,
        'url': u,
        'location': l,
    } for p, u, l in buying_offers_data]

    return {
        'stream': streaming_services_data,
        'rent': renting_offers_data,
        'buy': buying_offers_data,
    }

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
