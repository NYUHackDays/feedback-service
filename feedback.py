import requests, json, secrets

headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_key }



def sendEmail(eventId):
	r = requests.get('https://api.tnyu.org/v3/events/' + eventId + '?include=attendees', headers=headers, verify=False)
	if (r.status_code != 200): return
	r = json.loads(r.text)

	eboard_members = []
	attendees = []
	for post in r['included']:
		if post['attributes'].get('contact'):
			if post['attributes']['roles']:
				eboard_members.append(post['attributes']['contact']['email'])
				
			else:
				attendees.append(post['attributes']['contact']['email'])
	


	

def main():
	sendEmail('551482e3a3f1b49994cbc527')
main()
    

