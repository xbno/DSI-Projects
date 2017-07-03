#!flask/bin/python
import pandas as pd
import pickle
import flask
import re

app = flask.Flask(__name__)

# @app.route('/')
# def index():
#     return "Hello, World!"

#trained_models = pickle.load(open("trained_models_dict5.p", "rb"))
trained_models = pd.read_pickle("trained_models_dict5.p")

@app.route('/greet/<name>')
def greet(name):
    '''hey hey, whatsup'''
    return 'whatup, %s my dude?' %name

#working old
@app.route('/coefs', methods=["GET"])
def coefs():
    t = flask.request.args['t']
    model = flask.request.args['model']

    if t == '':
        t = '0'

    t = int(t)
    if t == 1:
        tplus = 'T\+1'
    elif t == 2:
        tplus = 'T\+2'
    elif t == 3:
        tplus = 'T\+3'
    else:
        tplus = ''

    keys = [key for key in list(trained_models.keys()) if re.findall(tplus,key)]
    keys = [key for key in keys if re.findall(model,key)]

    results = {}
    for key in keys:
        results[key] = trained_models[key]['coefs'].to_json()

    #return flask.jsonify({'a':t})
    return flask.jsonify(results)

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = '4000'
    app.run(HOST,PORT)
