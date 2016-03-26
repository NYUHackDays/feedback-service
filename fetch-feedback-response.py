import requests
import json
import secrets
import urlparse as ul

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


def fetch_survey_responses_from_survey_id(survey_id):
    res = requests.get('https://api.tnyu.org/v3/surveys/' +
                       survey_id, headers=headers)

    if r.status_code != 200:
        return

    r = res.json()
    uri_uid = r['data']['attributes']['URI'].split('/')[-1]
    survey = SurveyResponseCollection(
        survey_id, typeform_uri=uri_uid, typeform=True)
    return survey


class SurveyResponseCollection:

    def __init__(self, survey_id, **kwargs):
        self.survey_id = survey_id
        self.raw_responses = []
        self.raw_questions = []
        self.answers_by_person_id = {}
        self.typeformId_to_questionId = {}
        self.is_typeform = False

        if kwargs['typeform']:
            self.is_typeform = True
            self.get_typeform(kwargs['typeform_uri'])
            self.match_questions()
            self.generate_answers_from_form()

    def generate_answers_from_form(self):
        for person_id in self.answers_by_person_id.keys():
            if person_id is 'no_person_id':
                continue

            r = requests.get('https://api.tnyu.org/v3/people/' +
                             person_id, headers=headers)

            if r.status_code != 200:
                continue

            for answer_set in self.answers_by_person_id[person_id]:
                answer_id_collection = []

                for tid in answer_set.keys():
                    if tid not in self.typeformId_to_questionId:
                        continue
                    qid = self.typeformId_to_questionId[tid]
                    s = {}
                    s['data'] = {}
                    s['data']['type'] = 'answers'
                    s['data']['attributes'] = {}
                    s['data']['attributes']['answer'] = str(answer_set[tid])
                    s['data']['relationships'] = {}
                    s['data']['relationships']['question'] = {}
                    s['data']['relationships']['question']['data'] = {}
                    s['data']['relationships']['question'][
                        'data'] = {'type': 'questions', 'id': qid}
                    s = json.dumps(s)
                    res = requests.post(
                        'https://api.tnyu.org/v3/answers',
                        headers=headers, data=s
                    )
                    if r.status_code != 201:
                        print r.status_code
                        print('Can\'t genertate Answer for person_id: ' +
                              person_id)
                        print json.dumps(r.json(), indent=2)
                        return
                    r = res.json()
                    answer_id_collection.append(r['data']['id'])
                self.generate_surveyreponse(person_id, answer_id_collection)

    def generate_surveyreponse(self, person_id, answer_ids):
        s = {}
        s['data'] = {}
        s['data']['type'] = 'survey-responses'
        s['data']['attributes'] = {}
        s['data']['relationships'] = {}
        s['data']['relationships']['survey'] = {}
        s['data']['relationships']['survey']['data'] = {
            'type': 'survey', 'id': self.survey_id}
        s['data']['relationships']['respondent'] = {}
        s['data']['relationships']['respondent'][
            'data'] = {'type': 'person', 'id': person_id}
        s['data']['relationships']['answers'] = {}
        s['data']['relationships']['answers']['data'] = []
        for answer_id in answer_ids:
            s['data']['relationships']['answers']['data'].append(
                {
                    'type': 'answer',
                    'id': answer_id
                }
            )
        s = json.dumps(s)
        r = requests.post(
            'https://api.tnyu.org/v3/survey-responses',
            headers=headers,
            data=s
        )
        if r.status_code != 201:
            print 'Can\'t genertate Survey Responses Failed'
        r = json.dumps(r.json(), indent=2)
        print r

    def get_typeform(self, uid):
        res = requests.get('https://api.typeform.com/v0/form/' + uid +
                         '?key=' + secrets.tnyu_typeform_key +
                         '&completed=true')
        if r.status_code != 200:
            print 'Can\'t get Typeform API with uid: ' + uid
            print json.dumps(r.json(), indent=2)
            return

        r = res.json()

        self.raw_responses = r['responses']
        self.raw_questions = r['questions']
        collector_by_person_id = {}

        for response in self.raw_responses:
            meta = response['metadata']
            parsed = ul.urlparse(meta['referer'])
            collector_by_person_id[str(ul.parse_qs(parsed.query).get(
                'person_id', ['no_person_id'])[0])] = response['answers']
            # parsed_query_string = str(ul.parse_qs(parsed.query))
            # rsvpId = parsed_query_string.get('rsvpId', ['no_person_id'])[0]
            # collector_by_person_id[rsvpId] = response['answers']
            # use second one for all events past 11/23
            if person_id in collector_by_person_id:
                collector_by_person_id[person_id].append(response['answers'])
            else:
                collector_by_person_id[person_id] = []
        self.answers_by_person_id = collector_by_person_id

    def match_questions(self):
        res = requests.get(
            'https://api.tnyu.org/v3/questions/',
            headers=headers
        )

        if r.status_code != 200:
            print 'Can\'t get Question from Tech@NYU API'
            print json.dumps(r.json(), indent=2)
            return

        r = res.json()
        for tq in self.raw_questions:
            for question in r['data']:
                if question['attributes']['text'] == tq['question']:
                    self.typeformId_to_questionId[tq['id']] = question['id']

person_id = '54eb3fb77282d59a2b8bfa27'
sample_survey = '5636e651aa1f71de52159511'
test_survey = '5647fddebba8046463890779'
fetch_survey_responses_from_survey_id(test_survey)
