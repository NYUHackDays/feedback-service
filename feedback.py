import requests
import json
import secrets
import smtplib

headers = {
    'content-type': 'application/vnd.api+json',
    'accept': 'application/*, text/*',
    'authorization': 'Bearer ' + secrets.tnyu_api_key
}


def getEmails(eventId, event_data, eboard_members, attendees):
    r = requests.get('https://api.tnyu.org/v3/events/' + eventId +
                     '?include=attendees', headers=headers, verify=False)
    if (r.status_code != 200):
        return
    r = json.loads(r.text)
    event_data.append(r['data'])
    for post in r['included']:
        if post['attributes'].get('contact'):
            if post['attributes']['roles']:
                eboard_members.append(post)
            else:
                attendees.append(post)


def sendEmails(event_data, eboard_members, attendees, typeform_url):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(secrets.tnyu_email, secrets.tnyu_email_password)

    for i in range(0, len(eboard_members)):
        msg = "\r\n".join([
            "From: " + secrets.tnyu_email,
            "To: " + eboard_members[i]['attributes']['contact']['email'],
            "Subject: Thank you for coming to Tech@NYU's " +
            event_data[0]['attributes']['title'],
            "",
            'Hi, ' + eboard_members[i]['attributes']['name'] + '\n\n' +
            'We would appreciate some feedback: ' + typeform_url +
            '?personId=' + eboard_members[i]['id']
        ])
        server.sendmail(secrets.tnyu_email, eboard_members[i][
                        'attributes']['contact']['email'], msg)

    for j in range(0, len(attendees)):
        msg = "\r\n".join([
            "From: " + secrets.tnyu_email,
            "To: " + attendees[i]['attributes']['contact']['email'],
            "Subject: Thank you for coming to Tech@NYU's " +
            event_data[0]['attributes']['title'],
            "",
            'Hi, ' + attendees[i]['attributes']['name'] + '\n' +
            'Visit our website: ' + typeform_url +
            '?personId=' + attendees[i]['id']
        ])
        server.sendmail(secrets.tnyu_email, attendees[i][
                        'attributes']['contact']['email'], msg)

    server.quit()

if __name__ == '__main__':
    typeform_url = 'https://julieycpan.typeform.com/to/AN1E2o'
    eboard_members = []
    attendees = []
    event_data = []
    getEmails('561491ec9d262920f265190c',
              event_data, eboard_members, attendees)
    sendEmails(event_data, eboard_members, attendees, typeform_url)
