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
        hits = self.google.search(query)

        for indi in hits:
            for indj in indi:
                self.insert_hits(indj)

        self.area.chmode('NORMAL')

    def insert_hits(self, hit):
        self.area.append('%s\n' % hit['title'], '(YSX-TITLE)')
        self.area.append('%s\n' % hit['desc'], '(YSX-DESC)')
        self.area.append('%s\n\n' % hit['url'], '(YSX-URL)')

    def view(self, event):
        url = self.area.get_seq()
        mch = re.findall('questions/(.+)/', url)

        questions = self.get_question(mch[0])
        answers   = self.get_answers(mch[0])
        self.area.chmode('NORMAL')
        self.insert_data(questions, answers)

    def insert_data(self, questions, answers):
        area = root.note.create('none')

        area.delete('1.0', 'end')
        area.append('%s\n' % questions['items'][0]['title'], '(YSX-TITLE)')
        area.append('%s\n\n' % questions['items'][0]['body_markdown'], '(YSX-DESC)')
        area.append('By %s\n\n' % questions['items'][0]['owner']['display_name'], '(YSX-OWNER)')

        for ind in answers['items']:
            is_answer = ind.get('body_markdown')
            if is_answer:
                self.insert_answer(area, ind)
            else:
                self.insert_comment(area, ind)

    def insert_answer(self, area, answer):
        area.append('%s\n' % answer['body_markdown'], '(YSX-DESC)')
        area.append('By %s\n\n' % answer['owner']['display_name'], '(YSX-OWNER)')

    def insert_comment(self, area, comment):
        pass

    def get_question(self, id, order='desc', sort='activity', 
        site='stackoverflow', filter='!2uDdBASlzGE6U5lW)pVBlUm5WP0s37p*nnpd1zxfWA'):
        STACK_URL = 'https://api.stackexchange.com/2.2/questions/%s?/%s'
    
        params = {'order': order, 'sort': sort, 
        'site': site, 'filter': filter}
    
        url = STACK_URL % (id, urlencode(params))
        req = requests.get(url)
        return json.loads(req.text)

    def get_answers(self, question_id, order='desc', sort='activity', 
        site='stackoverflow', filter='!2uDdBASlzGE6U5lW)pVBlUm5WP0s37p*nnpd1zxfWA'):
        STACK_URL = 'https://api.stackexchange.com/2.2/questions/%s/answers?%s'

        params = {'order': order, 'sort': sort, 
        'site': site, 'filter': filter}
    
        url = STACK_URL % (question_id, urlencode(params))
        req = requests.get(url)
        return json.loads(req.text)

    def get_comments(id, order='desc', sort='activity', 
        site='stackoverflow', filter='!9YdnSJ*_T'):
        pass

install = Ysx
