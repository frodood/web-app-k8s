from flask import Flask, Response, send_from_directory, send_file, render_template
from scrapper import setup_metrics
from datetime import datetime
from pytz import timezone
import prometheus_client
import requests
import json, ast

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

app = Flask(__name__)
setup_metrics(app)

#requests to the application for "/homersimpson" receive a image of homersimpson as response
@app.route('/homersimpson/')
def get_simpson():
    filename ='homer-simpson.jpg'
    return send_file(filename, mimetype='image/jpg')

#requests to the application for "/covilha" receive local time in covilha as response
@app.route('/covilha/')
def get_time():
    format = "%Y-%m-%d %H:%M:%S %Z%z"
    #get local time in covilha using time zone
    now_utc = datetime.now(timezone('Europe/Lisbon'))
    return render_template('index.html', time=now_utc.strftime(format))


@app.route('/metrics')
def metrics():
    #expose the calculated metrics to prometheus
    return Response(prometheus_client.generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    #running on port 80
    app.run(host='0.0.0.0', port=80, debug=True)
