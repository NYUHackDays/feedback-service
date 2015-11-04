import requests, json, secrets, smtplib

headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_key }



def getEmails(eventId, eboard_members, attendees):
	r = requests.get('https://api.tnyu.org/v3/events/' + eventId + '?include=attendees', headers=headers, verify=False)
	if (r.status_code != 200): return
	r = json.loads(r.text)

	
	for post in r['included']:
		info = [post['id']]
		if post['attributes'].get('contact'):
			if post['attributes']['roles']:
				info.append(post['attributes']['contact']['email'])
				eboard_members.append(info)
				
			else:
				info.append(post['attributes']['contact']['email'])
				attendees.append(info)
	

def sendEmails(eboard_members, attendees):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(secrets.tnyu_email, secrets.tnyu_email_password)

	for i in range (0, len(eboard_members)):
		msg = 'Visit our website: https://julieycpan.typeform.com/to/AN1E2o?personId=' + eboard_members[i][0]
		server.sendmail(secrets.tnyu_email, eboard_members[i][1], msg)

	for j in range (0, len(attendees)):
		msg = 'Visit our website: https://julieycpan.typeform.com/to/AN1E2o?personId=' + eboard_members[i][0]
		server.sendmail(secrets.tnyu_email, eboard_members[i][1], msg)
		

	server.quit()
	



def main():
	#551482e3a3f1b49994cbc527
	eboard_members = []
	attendees = []
	getEmails('561491ec9d262920f265190c', eboard_members, attendees)

	print eboard_members
	print attendees

	sendEmails(eboard_members, attendees)

main()
    

