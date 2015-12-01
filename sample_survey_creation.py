import requests, json, secrets, patch_event

headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_key }

admin_headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_admin_key }

def post_question(text):
    q = {}
    q['data'] = {}
    q['data']['attributes'] = {}
    q['data']['attributes']['text'] = text
    q['data']['type'] = 'questions'
    q['data']['links'] = {}
    q = json.dumps(q)
    r = requests.post('https://api.tnyu.org/v3/questions', data=q, headers=headers, verify=False)
    print r.text
    if r.status_code != 200: return
    r = json.loads(r.text)
    return r['data']['id']

def post_survey(title, questions, addedby, form_uri, visible_to):
    s = {}
    s['data'] = {}
    s['data']['attributes'] = {}
    s['data']['attributes']['title'] = title
    s['data']['attributes']['URI'] = form_uri
    s['data']['attributes']['responsesVisibleTo'] = visible_to
    s['data']['type'] = 'surveys'
    s['data']['relationships'] = {}
    s['data']['relationships']['questions'] = {}
    s['data']['relationships']['questions']['data'] = []
    for qid in questions:
        s['data']['relationships']['questions']['data'].append({ 'type': 'questions', 'id': qid})
    s['data']['relationships']['addedBy'] = {}
    s['data']['relationships']['addedBy']['data'] = { 'type': 'people', 'id': addedBy }
    s = json.dumps(s)
    r = requests.post('https://api.tnyu.org/v3/surveys', data=s, headers=headers, verify=False)
    if r.status_code != 200: return
    r = json.loads(r.text)
    print r
    return r['data']['id']

questions = [
'5647fe7c9bf910ffbbcae5db',
'5647fe14f374f67c68805ff4',
'5647fe1de409e792e71e14e0',
'5647fe0d8599ac3a29754988',
'565d0d7a71c5442e2b136378',
'5647fe3e781d026d0b77695b',
'5647fe4b0dd50ccc027da8c1',
'5647fe54c64745a657ec39d1',
'5647fe685f92f23c34bc893b'
]
addedBy = '544195bba07c236a039e9016'
title = 'HackDays Feedback: Intro to Ruby on Rails'
uri = 'https://techatnyu.typeform.com/to/vXPXrJ'
visible_to = ['TEAM_MEMBER']
event_id = '56411efc23be829f1901e788'
# post_survey(title, questions, addedBy, uri, visible_to)
sid = '565d1088559f757f9d558d87'

patch_event.patch_event(event_id, survey=sid)

