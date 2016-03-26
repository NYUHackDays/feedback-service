import requests
import json
import secrets

headers = {
    'content-type': 'application/vnd.api+json',
    'accept': 'application/*, text/*',
    'authorization': 'Bearer ' + secrets.tnyu_api_key
}

admin_headers = {
    'content-type': 'application/vnd.api+json',
    'accept': 'application/*, text/*',
    'authorization': 'Bearer ' + secrets.tnyu_api_admin_key
}


def post_question(text):
    q = {}
    q['data'] = {}
    q['data']['attributes'] = {}
    q['data']['attributes']['text'] = text
    q['data']['type'] = 'questions'
    q['data']['links'] = {}
    q = json.dumps(q)
    res = requests.post('https://api.tnyu.org/v3/questions',
                        data=q, headers=headers, verify=False)

    if r.status_code != 200:
        return

    r = res.json()
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
        s['data']['relationships']['questions'][
            'data'].append({'type': 'questions', 'id': qid})
    s['data']['relationships']['addedBy'] = {}
    s['data']['relationships']['addedBy'][
        'data'] = {'type': 'people', 'id': addedBy}
    s = json.dumps(s)
    res = requests.post('https://api.tnyu.org/v3/surveys',
                        data=s, headers=headers, verify=False)
    if r.status_code != 200:
        return
    r = res.json()
    return r['data']['id']


def patch_event(event_id, sid):
    s = {}
    s['data'] = {}
    s['data']['attributes'] = {}
    s['data']['type'] = 'events'
    s['data']['id'] = event_id
    s['data']['relationships'] = {}
    s['data']['relationships']['survey'] = {}
    s['data']['relationships']['survey'][
        'data'] = {'type': 'surveys', 'id': sid}
    s = json.dumps(s)
    res = requests.patch('https://api.tnyu.org/v3/events/' +
                         event_id, data=s, headers=admin_headers, verify=False)
    r = res.json()


questions = ['5634fa8630cd1413fa0457a8', '5634fc3439a6828e0248737b']
addedBy = '544195bba07c236a039e9016'
title = '[TESTING INFRA] Sample Survey'
uri = 'https://julieycpan.typeform.com/to/AN1E2o'
visible_to = ['PUBLIC', 'INFRASTRUCTURE']
event_id = '561491ec9d262920f265190c'
sid = '5636e651aa1f71de52159511'

patch_event(event_id, sid)
