import requests, json, secrets
import urlparse as ul

headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_key }
admin_headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_admin_key }

def fetch_survey_responses_from_surveyId(survey_id):
    r = requests.get('https://api.tnyu.org/v3/surveys/' + survey_id, headers=headers)
    if (r.status_code != 200): return
    r = json.loads(r.text)
    uri_uid = r['data']['attributes']['URI'].split('/')[-1]
    survey = SurveyResponseCollection(survey_id, typeform_uri=uri_uid, typeform=True)

class SurveyResponseCollection:
    def __init__(self, surveyId, **kwargs):
        self.surveyId = surveyId
        self.raw_responses = []
        self.raw_questions = []
        self.answers_by_personId = {}
        self.typeformId_to_questionId = {}
        self.is_typeform = False
        if kwargs['typeform'] == True:
            self.is_typeform = True
            self.get_typeform(kwargs['typeform_uri'])
            self.match_questions()
            self.generate_answers_from_form()

    def generate_answers_from_form(self):
        # not working yet
        for personId in self.answers_by_personId.keys():
            if personId is 'no_personId': continue
            r = requests.get('https://api.tnyu.org/v3/people/' + personId, headers=headers)
            if r.status_code != 200: continue
            answerId_collection = []
            for tid in self.answers_by_personId[personId].keys():
                qid = self.typeformId_to_questionId[tid]
                s = {}
                s['data'] = {}
                s['data']['type'] = 'answers'
                s['data']['attributes'] = {}
                s['data']['attributes']['answer'] = self.answers_by_personId[personId][tid]
                s['data']['relationships'] = {}
                s['data']['relationships']['question'] = {}
                s['data']['relationships']['question']['data'] = {}
                s['data']['relationships']['question']['data'] = { 'type': 'questions', 'id': qid }
                s = json.dumps(s)
                r = requests.post('https://api.tnyu.org/v3/answers', headers=headers, data=s)
                if r.status_code != 200:
                    print 'Can\'t genertate Answer for personId: ' + personId
                    r = json.dumps(r.json(), indent=2)
                    print r
                    break
                r = json.loads(r.text)
                answerId_collection.append(r['data']['id'])
            self.generate_surveyreponse(personId, answerId_collection)

    def generate_surveyreponse(self, personId, answerIds):
        s = {}
        s['data'] = {}
        s['data']['type'] = 'survey-responses'
        s['data']['attributes'] = {}
        s['data']['relationships'] = {}
        s['data']['relationships']['survey'] = {}
        s['data']['relationships']['survey']['data'] = { 'type': 'survey', 'id': self.surveyId }
        s['data']['relationships']['respondent'] = {}
        s['data']['relationships']['respondent']['data'] = { 'type': 'person', 'id': personId }
        s['data']['relationships']['answers'] = {}
        s['data']['relationships']['answers']['data'] = []
        for answerId in answerIds:
            s['data']['relationships']['answers']['data'].append({ 'type': 'answer', 'id': answerId })
        s = json.dumps(s)
        r = requests.post('https://api.tnyu.org/v3/survey-responses', headers=headers, data=s)
        if r.status_code != 200:
            print 'Can\'t genertate Survey Responses Failed'
        r = json.dumps(r.json(), indent=2)
        print r



    def get_typeform(self, uid):
        r = requests.get('https://api.typeform.com/v0/form/' + uid + '?key=' + secrets.typeform_api_key + '&completed=true')
        if r.status_code != 200:
            print 'Can\'t get Typeform API with uid: ' + uid
            r = json.dumps(r.json(), indent=2)
            print r
            break
        r = json.loads(r.text)
        self.raw_responses = r['responses']
        self.raw_questions = r['questions']
        collector_by_personId = {}
        for response in self.raw_responses:
            meta = response['metadata']
            parsed = ul.urlparse(meta['referer'])
            collector_by_personId[str(ul.parse_qs(parsed.query).get('personId', ['no_personId'])[0])] = response['answers']
        self.answers_by_personId = collector_by_personId

    def match_questions(self):
        r = requests.get('https://api.tnyu.org/v3/questions/', headers=headers)
        if r.status_code != 200:
            print 'Can\'t get Question from Tech@NYU API'
            r = json.dumps(r.json(), indent=2)
            print r
            break
        r = json.loads(r.text)
        for tq in self.raw_questions:
            for question in r['data']:
                if question['attributes']['text'] == tq['question']:
                    self.typeformId_to_questionId[tq['id']] = question['id']



sample_survey = '5636e651aa1f71de52159511'
fetch_survey_responses_from_surveyId(sample_survey)

r = requests.get('https://api.tnyu.org/v3/survey-responses', headers=admin_headers)
r = json.dumps(r.json(), indent=2)
print r

r = requests.get('https://api.tnyu.org/v3/answers', headers=admin_headers)
r = json.dumps(r.json(), indent=2)
print r

