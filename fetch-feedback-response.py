import requests, json, secrets
import urlparse as ul

# testing from db-backup
headers = {'content-type': 'application/vnd.api+json', 'accept': 'application/*, text/*', 'authorization': 'Bearer ' + secrets.tnyu_api_key }

def fetch_survey_response_typeform(survey_id):
    r = requests.get('https://api.tnyu.org/v3/surveys/' + survey_id, headers=headers)
    if (r.status_code != 200): return
    r = json.loads(r.text)
    uri_uid = r['data']['attributes']['URI'].split('/')[-1]
    survey = SurveyResponse(uri_uid, typeform=True, visibleTo=['PUBLIC', 'INFRASTRUCTURE'])


class SurveyResponse:
    def __init__(self, *args, **kwargs):
        self.raw_responses = []
        self.raw_questions = []
        self.answers_by_personId = {}
        self.typeformId_to_questionId = {}
        self.isTypeform = False
        self.visibleTo = kwargs.get('visibleTo', [])
        if len(args) == 1 and kwargs['typeform'] == True:
            self.get_typeform(args[0])
            self.match_questions()
            self.generate_answer_obj
            self.isTypeform = True

    def generate_answer_obj(self):
        # this doesn't work yet
        for personId in self.answers_by_personId.keys():
            if personId is 'no_personId': break
            # check personId in api
            r = requests.get('https://api.tnyu.org/v3/people/' + personId, headers=headers)
            if (r.status_code != 200): break

            for tid in self.answers_by_personId[personId].keys():
                qid = self.typeformId_to_questionId[tid]
                s = {}
                s['data'] = {}
                s['data']['type'] = 'answers'
                s['data']['attributes'] = {}
                s['data']['attributes']['responsesVisibleTo'] = self.visibleTo
                s['data']['relationships'] = {}
                s['data']['relationships']['questions'] = {}
                s['data']['relationships']['question']['data'] = { 'type': 'questions', 'id': qid }
                s['data']['attributes']['answer'] = self.answers_by_personId[personId][tid]
                s = json.dumps(s)
                r = requests.post('https://api.tnyu.org/v3/answers', headers=headers, data=s)
                print r


    def get_typeform(self, uid):
        url = 'https://api.typeform.com/v0/form/' + uid + '?key=' + secrets.typeform_api_key + '&completed=true'
        r = requests.get(url)
        if (r.status_code != 200): return
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
        r = json.loads(r.text)
        for tq in self.raw_questions:
            for question in r['data']:
                if question['attributes']['text'] == tq['question']:
                    self.typeformId_to_questionId[tq['id']] = question['id']



sample_survey = '5636e651aa1f71de52159511'
fetch_survey_response_typeform(sample_survey)

# survey = SurveyResponse('AN1E2o')
# print survey.answers_by_personId
