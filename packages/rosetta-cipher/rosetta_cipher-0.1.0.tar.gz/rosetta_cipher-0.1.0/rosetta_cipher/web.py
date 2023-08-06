from flask import Flask, request
from rosetta_cipher import cipher
import json


app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/random', methods=['GET'])
def random():
    length = request.args.get('length', default=2, type=int)
    retry = request.args.get('retry', default=0, type=int)
    separator = request.args.get('separator', default='_', type=str)
    capitalize = request.args.get('capitalize', default=False, type=bool)
    return json.dumps(cipher.get_random_name(
        length=length,
        retry=retry,
        separator=separator,
        capitalize=capitalize
    ))


@app.route('/name/<obj>', methods=['GET'])
@app.route('/<obj>', methods=['GET'])
def name(obj):
    length = request.args.get('length', default=2, type=int)
    retry = request.args.get('retry', default=0, type=int)
    separator = request.args.get('separator', default='_', type=str)
    capitalize = request.args.get('capitalize', default=False, type=bool)
    return json.dumps(cipher.get_name(
        obj=obj,
        length=length,
        retry=retry,
        separator=separator,
        capitalize=capitalize
    ))


@app.route('/version', methods=['GET'])
def version():
    return json.dumps(cipher.get_version())
