from flask import Flask, Response, send_from_directory, send_file, render_template
from scrapper import setup_metrics
import prometheus_client
import requests
import json, ast


CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')


app = Flask(__name__)
setup_metrics(app)

@app.route('/homersimpson/')
def get_simpson():
    filename ='homer-simpson.jpg'
    return send_file(filename, mimetype='image/jpg')

@app.route('/covilha/')
def get_time():
    headers = {'Content-type': 'application/json'}
    url = 'http://api.worldweatheronline.com/premium/v1/tz.ashx?key=895d2154a29b4830b2693625182408&q=covilha&format=json'
    response = requests.get(url, headers=headers)
    if (response.ok):
        jdata = ast.literal_eval(json.dumps(json.loads(response.content)))
        print(jdata)
        city = jdata['data']['request'][0]['query']
        localtime = jdata['data']['time_zone'][0]['localtime']
        return render_template('index.html', time=str(localtime))

    else:
        response.raise_for_status()

@app.route('/metrics')
def metrics():
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
