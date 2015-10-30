import requests, json, secrets
import urlparse as ul

# testing from db-backup
headers = {'content-type': 'application/vnd.api+json; ext=bulk'}
event = 'https://api.tnyu.org/v3/events/' 

def fetch_survey_response(event_id):
    r = requests.get(event + event_id, headers=headers)
    if (r.status_code != 200): return
    r = json.loads(r.text)

    # get surveyId from event, this might change
    if 'surveyId' in r['data']:
        surveyId = r['data']['surveyId']

# fetch_survey_response('561491ec9d262920f265190c');
# print secrets.typeform_api_key

def get_typeform(uid):
    url = 'https://api.typeform.com/v0/form/' + uid + '?key=' + secrets.typeform_api_key + '&completed=true'
    r = requests.get(url)
    if (r.status_code != 200): return
    r = json.loads(r.text)
    responses = r['responses']
    questions = r['questions']
    collector_by_personId = {}

    for response in responses:
        meta = response['metadata']
        parsed = ul.urlparse(meta['referer'])
        collector_by_personId[str(ul.parse_qs(parsed.query).get('personId', ['no_personId'])[0])] = response['answers']
    print collector_by_personId

def match_questions():
    url = 'https://api.tnyu.org/v3/questions'
    r = requests.get(url)

get_typeform('AN1E2o')
