import requests, json, secrets

headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_key }

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
    return r['data']['id']

questions = ['5634fa8630cd1413fa0457a8','5634fc3439a6828e0248737b']
addedBy = '544195bba07c236a039e9016'
title = '[TESTING INFRA] Sample Survey'
uri = 'https://julieycpan.typeform.com/to/AN1E2o'
visible_to = ['PUBLIC', 'INFRASTRUCTURE']

