import requests, json, secrets

headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': ('Bearer', secrets.tnyu_api_key)}
# r = requests.get('https://api.tnyu.org/v3/people', headers=headers, verify=False)
# data = json.loads(r.text)
# print data

q = { 'text': '[TESTING] What is your name?' }
q = json.dumps(q)

r = requests.get('https://api.tnyu.org/v3/questions', data=q, headers=headers, verify=False)
print r.text
# survey = {
#         title: 'Sample Survey for Testing',
#         }
