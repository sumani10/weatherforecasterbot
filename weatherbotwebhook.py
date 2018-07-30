import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response


## flask app should start in global layout

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  print( json.dumps(req, indent=4))

  res = makeResponse(req)
  res = json.dumps(res, indent=4)
  r = make_response(res)
  r.headers['Content-type'] = 'application/json'
  return

def makeResponse(req):
  result = req.get('result')
  parameters = result.get('parameters')
  city = parameters.get('geo-city')
  date = parameters.get('date')

  r=requests.get('https://api.openweathermap.org/data/2.5/forecast?q=' + city +'&appid=ebf857629c73568a1f4f4ee035c5db79')
  json_object = r.json()
  weather = json_object['list']

  for i in range(0,30):
    if date in weather[i]['dt_txt']:
      condition = weather[i]['weather'][0]['description']
      break



  speech = "The forecast for" + city + " for " + date + " is " + condition

  return {
    "speech" : speech,
    "displayText" : speech,
    "source" : "apiai-weather-webhook"
  }

  if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    print('Starting app on port %d' % (port))
    app.run(deubg=False, port=port, host='0.0.0.0')
