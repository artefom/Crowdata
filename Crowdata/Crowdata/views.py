"""
Routes and views for the flask application.
"""

from flask import jsonify
from datetime import datetime
from flask import render_template
from Crowdata import app
import json

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

circles = [
    {
        'latitude': 55,
        'longitude': 45,
        'radius': 3,
        'value': 25,
        'NumOfPlaces': 3,
        'UrlToImage': "http://www.konbini.com/fr/files/2015/08/Lol-Graphics-32-810x485.gif"
    },
    {
        'latitude': 53,
        'longitude': 46,
        'radius': 5,
        'value': 2,
        'NumOfPlaces': 2,
        'UrlToImage': "http://www.konbini.com/fr/files/2015/08/Lol-Graphics-32-810x485.gif"
    },
    {
        'latitude': 51,
        'longitude': 42,
        'radius': 7,
        'value': 25,
        'NumOfPlaces': 1,
        'UrlToImage': "http://www.konbini.com/fr/files/2015/08/Lol-Graphics-32-810x485.gif"
    },
    {
        'latitude': 56,
        'longitude': 44,
        'radius': 7,
        'value': 10,
        'NumOfPlaces': 4,
        'UrlToImage': "http://www.konbini.com/fr/files/2015/08/Lol-Graphics-32-810x485.gif"
    }
]


@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/circles')
def get_tasks():
    text = json.dumps(circles, separators=(',', ':'))
    #text = jsonify({'tasks': tasks})
    return text


#@app.route('/api/v1.0/test', methods=['GET'])
#def get_tasks():
#    text = "hello"
#    return text