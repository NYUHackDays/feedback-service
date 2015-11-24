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


def sendEmails(event_data, survey_link, eboard_members, attendees):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(secrets.tnyu_email, secrets.tnyu_email_password)

    for i in range(0, len(eboard_members)):

        msg = "\r\n".join([
            'Hi ' + eboard_members[i]['attributes']['name'] + '!\n\n' +
            'Thanks for coming out! We are constantly looking to improve ' +
            'on our events, and we would really appreciate it if you ' +
            'could take two minutes out of your day to fill out our' +
            'feedback form. We\'d love to know how we could do better: ' +
            survey_link + '?rsvpId=' + eboard_members[i]['id'],
            '',
            'Filling the form out will give us an idea of how everything ' +
            'went and if there was something you really liked about the ' +
            'event or something you did not like.\n',
            'Feel free to email feedback@techatnyu.org if you have ' +
            'other questions or concerns.',
            '',
            'Thank you,',
            'Tech@NYU team'
        ])
        print msg
        try:
            server.sendmail(secrets.tnyu_email, eboard_members[i][
                            'attributes']['contact']['email'], msg)
        except UnicodeEncodeError:
            continue

    for j in range(0, len(attendees)):
        msg = "\r\n".join([
            "From: " + secrets.tnyu_email,
            "To: " + attendees[j]['attributes']['contact']['email'],
            "Subject: Thank you for coming to Tech@NYU's " +
            event_data[0]['attributes']['title'],
            '',
            'Hi ' + attendees[j]['attributes']['name'] + '!\n\n' +
            'Thanks for coming out! We are constantly looking to improve ' +
            'on our events, and we would really appreciate it if you could ' +
            ' take two minutes out of your day to fill out our feedback ' +
            'form. We\'d love to know how we could do better: ' +
            survey_link + '?rsvpId=' + attendees[j]['id'],
            '',
            'Filling the form out will give us an idea of how everything ' +
            'went and if there was something you really liked about the ' +
            'event or something you did not like.\n',
            'Feel free to email feedback@techatnyu.org if you have other ' +
            'questions or concerns.',
            '',
            'Thank you,',
            'Tech@NYU team'
        ])
        print msg
        try:
            server.sendmail(secrets.tnyu_email, attendees[j][
                            'attributes']['contact']['email'], msg)
        except UnicodeEncodeError:
            print 'UnicodeEncodeError:' + attendees[j]
            continue

    server.quit()


def main():
    event_id = '5644e5e37af46de029dfb9f9'
    eboard_members = []
    attendees = []
    event_data = []
    survey_link = 'https://techatnyu.typeform.com/to/ElE6F5'
    print attendees[0]
    getEmails(event_id, event_data, eboard_members, attendees)
    sendEmails(event_data, survey_link, eboard_members, attendees)
main()
