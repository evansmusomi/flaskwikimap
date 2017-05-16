""" Defines data structures to use to read and write to tables """

import json
import urllib

from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """ Defines data structure for reading and writing to users table """

    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        """ Generates password hash from password """
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        """ Compares password hash with password """
        return check_password_hash(self.pwdhash, password)


class Place(object):
    """ Defines model for fetching places from API """

    def meters_to_walking_time(self, meters):
        """ Converts meters to walking time """
        return int(meters / 80)

    def wiki_path(self, slug):
        """ Replace spaces with _ in search urls """
        return urllib.parse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

    def address_to_latlng(self, address):
        """ Converts address into geo-coordinates """

        address = urllib.request.quote(address)

        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=false'.format(
            address)
        g = urllib.request.urlopen(url)
        results = g.read()
        g.close()

        location = json.loads(results)['results'][0]['geometry']['location']
        return (location['lat'], location['lng'])

    def query(self, address):
        """ Gets places of interest near an address """

        lat, lng = self.address_to_latlng(address)

        query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(
            lat, lng)
        g = urllib.request.urlopen(query_url)
        results = g.read()
        g.close()

        data = json.loads(results)

        places = []
        for place in data['query']['geosearch']:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lng = place['lon']

            wiki_url = self.wiki_path(name)
            walking_time = self.meters_to_walking_time(meters)

            destination = {
                'name': name,
                'url': wiki_url,
                'time': walking_time,
                'lat': lat,
                'lng': lng
            }

            places.append(destination)

        return places
