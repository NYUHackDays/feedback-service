import requests, json, secrets, smtplib


headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_key }


def getEmails(eventId, event_data, eboard_members, attendees):
	r = requests.get('https://api.tnyu.org/v3/events/' + eventId + '?include=attendees', headers=headers, verify=False)
	if (r.status_code != 200): return
	r = json.loads(r.text)

	event_data.append(r['data'])
	
	for post in r['included']:
		if post['attributes'].get('contact'):
			if post['attributes']['roles']:
				eboard_members.append(post)			
			else:
				attendees.append(post)
	

def sendEmails(event_data, survey_link, eboard_members, attendees):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(secrets.tnyu_email, secrets.tnyu_email_password)

	for i in range (0, len(eboard_members)):

		msg = "\r\n".join([
			"From: " + secrets.tnyu_email,
			"To: " + eboard_members[i]['attributes']['contact']['email'],
			"Subject: Thank you for coming to Tech@NYU's " + event_data[0]['attributes']['title'],
			"",
			'Hi, ' + eboard_members[i]['attributes']['name'] + '\n\n' +
                        'Thanks for coming out! We\'d love to know how we could do better: ' + survey_link + '?personId=' + eboard_members[i]['id']
		])
		print msg
		server.sendmail(secrets.tnyu_email, eboard_members[i]['attributes']['contact']['email'], msg)

	for j in range (0, len(attendees)):
		msg = "\r\n".join([
			"From: " + secrets.tnyu_email,
			"To: " + attendees[j]['attributes']['contact']['email'],
			"Subject: Thank you for coming to Tech@NYU's " + event_data[0]['attributes']['title'],
			"",
			'Hi, ' + attendees[j]['attributes']['name'] + '\n\n' +
                        'Thanks for coming out! We\'d love to know how we could do better: ' + survey_link + '?personId=' + attendees[j]['id']
		])
		print msg
		server.sendmail(secrets.tnyu_email, attendees[j]['attributes']['contact']['email'], msg)
		
	server.quit()

def main():
        event_id = '5644e5e37af46de029dfb9f9'
	eboard_members = []
	attendees = []
        event_data = []
        survey_link = 'https://techatnyu.typeform.com/to/ElE6F5'
	getEmails(event_id, event_data, eboard_members, attendees)
	sendEmails(event_data, survey_link, eboard_members, attendees)
main()
    

