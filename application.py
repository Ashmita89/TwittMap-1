from flask import Flask
from flask import render_template
from pyes import *
from flask import request
import json
import requests
from wsgiref.simple_server import make_server
import flask_googlemaps


# Address of the elasticsearch host
elasticsearchURL = 'https://search-twittmap-77ta2y45lfunfg4hhdxaezl524.us-west-2.es.amazonaws.com'
application = Flask(__name__)
application.config['GOOGLEMAPS_KEY']="AIzaSyC403JgsSdPSph8zoqbPs9DMzkLosIRD6o"
flask_googlemaps.GoogleMaps(application)

res_count = requests.get(elasticsearchURL + '/test-index/test-type/_count')
count_json = json.loads(res_count.text)

@application.route('/',methods=['POST'])
def backend_query():
    dd_select = request.form['keyword_drop_down']
    selected = dd_select
    conn = ES(['https://search-twittmap-77ta2y45lfunfg4hhdxaezl524.us-west-2.es.amazonaws.com'])
    q=TermQuery("message",dd_select)
    results=conn.search(query=q)
    print (results)
    coord_list = []
    for i in results:
        if (i["location"]["lat"]) is not None:
            print (i)
            coordinates = str(i["location"]["lat"])+","+str(i["location"]["lon"])
            coord_list.append(coordinates)

    return render_template('MapUI.html', count = count_json['count'], coord_list =  coord_list, selected = selected)

@application.route('/', methods=['GET','POST'])
def home():
     return render_template('MapUI.html', count = count_json['count'], coord_list = [])


if __name__ == '__main__':
     application.run(host='127.0.0.1')
     make_server("LowCost-env.zpivveuucj.us-west-2.elasticbeanstalk.com", application).serve_forever()