from urllib.parse import urlencode
from vyapp.ask import Ask, Get
from vyapp.app import root
from subprocess import check_output
import requests
import json
import re


class Ysx:
    TAGCONF = {
    '(YSX-TITLE)': {'foreground': '#FFAF33'},
    '(YSX-DESC)': {'foreground': '#DCDFD9'},
    '(YSX-URL)': {'foreground': '#7FEDA9'},
    '(YSX-OWNER)': {'foreground': '#AFFF33'}}

    def __init__(self, area):
        area.install('ysx', ('EXTRA', '<Key-slash>', self.find),
        ('EXTRA', '<Key-question>',  self.view))

        self.area = area
        self.area.tags_config(self.TAGCONF)

    def find(self, event):
        ask   = Ask()
        self.area.delete('1.0', 'end')
        data = check_output(['googler', '--json', '-w', 
        'https://stackoverflow.com', ask.data])

        hits = json.loads(data)
        for ind in hits:
            self.insert_hits(ind)

        self.area.chmode('NORMAL')

    def insert_hits(self, hit):
        self.area.append('%s\n' % hit['title'], '(YSX-TITLE)')
        self.area.append('%s\n' % hit['abstract'], '(YSX-DESC)')
        self.area.append('%s\n\n' % hit['url'], '(YSX-URL)')

    def view(self, event):
        REG = 'q[uestion]+/([0-9]+)/?'
        url = self.area.get_line()
        mch = re.search(REG, url)

        question_id = mch.group(1)
        question    = self.get_question(question_id)
        question    = question['items'][0]
        # answers     = self.get_answers(question_id)
        answers     = question['answers']

        comments    = question['comments']

        self.area.chmode('NORMAL')

        area = root.note.create('none')
        area.delete('1.0', 'end')

        title = question['title']
        title = 'Question title: %s\n' % title

        markdown = question['body_markdown']
        markdown = '%s\n\n' % markdown

        owner = question['owner']['display_name']
        owner = 'Question owner: %s\n' % owner

        area.append(owner, '(YSX-OWNER)')
        area.append(title, '(YSX-TITLE)')
        area.append(markdown, '(YSX-DESC)')

        area.append('Comments:\n')

        for ind in comments:
            self.insert_question_comment(area, ind)

        for ind in answers:
            self.insert_answer(area, ind)

    def insert_answer(self, area, answer):
        markdown = answer.get('body_markdown')
        markdown = '%s\n' % markdown
        owner    = answer.get('owner')
        owner    = owner.get('display_name')
        owner    = '\nAnswer owner: %s\n' % owner

        area.append(owner, '(YSX-OWNER)')
        area.append(markdown, '(YSX-DESC)')

    def insert_question_comment(self, area, comment):
        markdown = comment.get('body_markdown')
        markdown = '%s\n' % markdown
        owner    = comment.get('owner')
        owner    = owner.get('display_name')
        owner    = 'Comment owner: %s\n' % owner

        area.append(markdown, '(YSX-DESC)')
        area.append(owner, '(YSX-OWNER)')

    def get_answers_comments(self, answer_ids):
        pass

    def get_question_comments(self, question_id):
        URL = 'https://api.stackexchange.com/2.2/questions/%s?/comments/%s'
    
        params = {'order': 'desc', 'sort': 'activity', 'site': 'stackoverflow', 
        'filter': '!187D_k.dW21CE4wnVmvCCHjNi1rEqE0P7SF3wsJUVl*oQQ8(zCjIIa34WstVfI'}
    
        url = URL % (question_id, urlencode(params))
        req = requests.get(url)
        return json.loads(req.text)

    def get_question(self, question_id):
        URL = 'https://api.stackexchange.com/2.2/questions/%s?/%s'
    
        params = {'order': 'desc', 'sort': 'activity', 'site': 'stackoverflow', 
        'filter': '!187D_k.dW21CE4wnVmvCCHjNi1rEqE0P7SF3wsJUVl*oQQ8(zCjIIa2yLgA_jn'}
    
        url = URL % (question_id, urlencode(params))
        req = requests.get(url)
        return json.loads(req.text)

    def get_answers(self, question_id):
        URL = 'https://api.stackexchange.com/2.2/questions/%s/answers?%s'
        params = {'order': 'desc', 'sort': 'activity', 'site': 'stackoverflow', 
        'filter': '!WyX5UezTc0C3EZPZ*F2m.(TE3yxC7yJisQjzoZj'}

        url = URL % (question_id, urlencode(params))
        req = requests.get(url)
        return json.loads(req.text)

install = Ysx


