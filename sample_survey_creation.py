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
    return r['data']['id']

# def patch_event(event_id, sid):
#     s = {}
#     s['data'] = {}
#     s['data']['attributes'] = {}
#     s['data']['type'] = 'events'
#     s['data']['id'] = event_id
#     s['data']['relationships'] = {}
#     s['data']['relationships']['survey'] = {}
#     s['data']['relationships']['survey']['data'] = { 'type': 'surveys', 'id': sid }
#     s = json.dumps(s)
#     r = requests.patch('https://api.tnyu.org/v3/events/' + event_id, data=s, headers=admin_headers, verify=False)
#     r = json.loads(r.text)
#     print r


questions = ['5647fe7c9bf910ffbbcae5db', '5647fe3e781d026d0b77695b', '5647fe4b0dd50ccc027da8c1', '5647fe54c64745a657ec39d1', '5647fe685f92f23c34bc893b']
addedBy = '544195bba07c236a039e9016'
title = 'DesignDays Feedback: Getting Started with UX Design'
uri = 'https://techatnyu.typeform.com/to/ElE6F5'
visible_to = ['TEAM_MEMBER']
event_id = '5644e5e37af46de029dfb9f9'
# sid = post_survey(title, questions, addedBy, uri, visible_to)
# print sid
sid = '565cf89dd63f91df12e14ebd'

patch_event.patch_event(event_id, survey=sid)

