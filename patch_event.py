import requests, json, secrets, sys
headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_key }
admin_headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_admin_key }

def patch_event(eventId, title=None, shortTitle=None, description=None, detail=None, level=None, venue=None, venueId=None, survey=None, teams=[], coorganizers=[], presenters=[], attendees=[], rsvps=[], feedback=[], teaches=[]):
    s = {}
    s['data'] = {}
    s['data']['type'] = 'events'
    s['data']['id'] = eventId
    s['data']['attributes'] = {}
    s['data']['attributes']['aims'] = []
    if title != None: s['data']['attributes']['title'] = title
    if shortTitle != None: s['data']['attributes']['shortTitle'] = shortTitle
    if description != None: s['data']['attributes']['description'] = description
    if detail != None: s['data']['attributes']['detail'] = detail
    if level != None: s['data']['attributes']['level'] = level
    s['data']['relationships'] = {}
    if venueId != None:
        s['data']['relationships']['venue'] = {}
        s['data']['relationships']['venue']['data'] = {'type': 'venues', 'id': venueId}
    if survey != None:
        s['data']['relationships']['survey'] = {}
        s['data']['relationships']['survey']['data'] = {'type': 'surveys', 'id': survey}
    if len(teams) > 0:
        s['data']['relationships']['teams'] = {}
        s['data']['relationships']['teams']['data'] = []
        for teamId in teams:
            s['data']['relationships']['teams']['data'].append({'type': 'teams', 'id': teamId})
    if len(coorganizers) > 0:
        s['data']['relationships']['coorganizers'] = {}
        s['data']['relationships']['coorganizers']['data'] = []
        for orgId in coorganizers:
            s['data']['relationships']['coorganizers']['data'].append({'type': 'organizations', 'id': orgId})
    if len(presenters) > 0:
        s['data']['relationships']['presenters'] = {}
        s['data']['relationships']['presenters']['data'] = []
        for personId in presenters:
            s['data']['relationships']['presenters']['data'].append({'type': 'people', 'id': personId})
    if len(attendees) > 0:
        s['data']['relationships']['attendees'] = {}
        s['data']['relationships']['attendees']['data'] = []
        for personId in attendees:
            s['data']['relationships']['attendees']['data'].append({'type': 'people', 'id': personId})
    if len(rsvps) > 0:
        s['data']['relationships']['rsvps'] = {}
        s['data']['relationships']['rsvps']['data'] = []
        for personId in rsvps:
            s['data']['relationships']['rsvps']['data'].append({'type': 'people', 'id': personId})
    if len(feedback) > 0:
        s['data']['relationships']['feedback'] = {}
        s['data']['relationships']['feedback']['data'] = []
        for surveyResponseId in feedback:
            s['data']['relationships']['feedback']['data'].append({'type': 'surveyResponses', 'id': surveyResponseId})
    if len(teaches) > 0:
        s['data']['relationships']['teaches'] = {}
        s['data']['relationships']['teaches']['data'] = []
        for skillId in teaches:
            s['data']['relationships']['teaches']['data'].append({'type': 'skills', 'id': skillId})
    s = json.dumps(s)
    r = requests.patch('https://api.tnyu.org/v3/events/' + eventId, data=s, headers=admin_headers, verify=False)
    r = json.loads(r.text)
    print r['data']['id']


eventId = '5626b985534ba411491a5f4c'

# with open(sys.argv[1], 'r') as f:
#     words = []
#     for line in f:
#         words.append(line.strip())

# print words

# patch_event(eventId, words)
