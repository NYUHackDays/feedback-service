import requests, json

headers = {'content-type': 'application/vnd.api+json; ext=bulk'}
event = 'http://localhost:8000/v3/events/' 

def fetch_survey_response(event_id):
    r = requests.get(event + event_id, headers=headers)
    if (r.status_code != 200):
        return
    r = json.loads(r.text)
    print r['data']

fetch_survey_response('561491ec9d262920f265190c');
