import pickle
import requests
import json
import numpy as np
import weakref
import math
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians
import time

"""
This script runs the Crowdata application using a development server.
"""

from os import environ
from Crowdata import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
