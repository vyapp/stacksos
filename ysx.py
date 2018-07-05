from urllib.parse import urlencode
import requests
from vyapp.ask import Ask, Get
from vyapp.app import root
from gle import Google
import json
import re


class Ysx:
    TAGCONF = {
    '(YSX-TITLE)': {'foreground': '#FFAF33'},
    '(YSX-DESC)': {'foreground': '#33B2FF'},
    '(YSX-URL)': {'foreground': '#7FEDA9'},
    '(YSX-COMMENT)': {'foreground': '#7FEDA9'},
    '(YSX-OWNER)': {'foreground': '#A9BFB1'}}

    def __init__(self, area):
        area.install('ysx', ('ALPHA', '<Control-x>', self.find),
        ('ALPHA', '<Key-x>',  self.view))

        self.area = area
        self.area.tags_config(self.TAGCONF)
        self.google  = Google(count=2)

    def find(self, event):
        ask   = Ask()
        self.area.delete('1.0', 'end')
        query = 'stackoverflow %s' % ask.data
        hits  = self.google.search(query)
        REG   = 'stackoverflow.+/q[uestion]+/([0-9]+)/?'

        for indi in hits:
            for indj in indi:
                if re.search(REG, indj['url']):
                    self.insert_hits(indj)

        self.area.chmode('NORMAL')

    def insert_hits(self, hit):
        self.area.append('%s\n' % hit['title'], '(YSX-TITLE)')
        self.area.append('%s\n' % hit['desc'], '(YSX-DESC)')
        self.area.append('%s\n\n' % hit['url'], '(YSX-URL)')

    def view(self, event):
        REG = 'q[uestion]+/([0-9]+)/?'
        url = self.area.get_seq()
        mch = re.search(REG, url)
        question_id = mch.group(1)
        questions   = self.get_question(question_id)
        answers     = self.get_answers(question_id)

        self.area.chmode('NORMAL')

        area = root.note.create('none')
        area.delete('1.0', 'end')

        area.append('%s\n' % questions['items'][0]['title'], '(YSX-TITLE)')
        area.append('%s\n\n' % questions['items'][0]['body_markdown'], '(YSX-DESC)')
        area.append('By %s\n\n' % questions['items'][0]['owner']['display_name'], '(YSX-OWNER)')
        items = answers['items']

        for ind in items:
            if ind.get('body_markdown'):
                self.insert_answer(area, ind)
            else:
                self.insert_comment(area, ind)

    def insert_answer(self, area, answer):
        area.append('%s\n' % answer['body_markdown'], '(YSX-DESC)')
        area.append('By %s\n\n' % answer['owner']['display_name'], '(YSX-OWNER)')

    def insert_comment(self, area, comment):
        pass

    def get_question(self, question_id, order='desc', sort='activity', 
        site='stackoverflow', filter='!WyX5UezTc0C3EZPZ*F2m.(TE3yxC7yJisQjzoZj'):
        STACK_URL = 'https://api.stackexchange.com/2.2/questions/%s?/%s'
    
        params = {'order': order, 'sort': sort, 
        'site': site, 'filter': filter}
    
        url = STACK_URL % (question_id, urlencode(params))
        req = requests.get(url)
        return json.loads(req.text)

    def get_answers(self, question_id, order='desc', sort='activity', 
        site='stackoverflow', filter='!WyX5UezTc0C3EZPZ*F2m.(TE3yxC7yJisQjzoZj'):
        STACK_URL = 'https://api.stackexchange.com/2.2/questions/%s/answers?%s'

        params = {'order': order, 'sort': sort, 
        'site': site, 'filter': filter}
    
        url = STACK_URL % (question_id, urlencode(params))
        req = requests.get(url)
        return json.loads(req.text)

install = Ysx
