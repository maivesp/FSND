import os
from flask import Flask, request, abort, jsonify

from models import *

@app.route('/')
def fun():
    return("Hello World")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)