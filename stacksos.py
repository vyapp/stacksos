from urllib.parse import urlencode
from vyapp.ask import Ask, Get
from vyapp.app import root
from subprocess import check_output
import requests
import json
import re
import html

class StackSOS:
    TAGCONF = {
    '(YSX-TITLE)': {'foreground': '#FFAF33'},
    '(YSX-DESC)': {'foreground': '#DCDFD9'},
    '(YSX-URL)': {'foreground': '#7FEDA9'},
    '(YSX-OWNER)': {'foreground': '#AFFF33'}}

    def __init__(self, area):
        area.install('ysx', ('EXTRA', '<Control-w>', self.find),
        ('EXTRA', '<Key-W>',  self.view_question))

        self.area = area
        self.area.tags_config(self.TAGCONF)

    def find(self, event):
        root.status.set_msg('Search Topic:')
        ask  = Ask()

        data = check_output(['googler', '--json', '-w', 
        'https://stackoverflow.com', ask.data])

        area = root.note.create('(?) %s...' % ask.data[:15])
        hits = json.loads(data)

        for ind in hits:
            self.insert_hits(area, ind)
        self.area.chmode('NORMAL')
        root.status.set_msg('Found %s links.' % len(hits))

    def insert_hits(self, area, hit):
        area.append('%s\n' % hit['title'], '(YSX-TITLE)')
        area.append('%s\n' % hit['abstract'], '(YSX-DESC)')
        area.append('%s\n\n' % hit['url'], '(YSX-URL)')

    def view_question(self, event):
        REG = 'q[uestion]+/([0-9]+)/?'
        url = self.area.get_line()
        mch = re.search(REG, url)

        question_id = mch.group(1)
        question    = self.get_question(question_id)
        question    = question['items'][0]

        self.area.chmode('NORMAL')

        title = question['title']
        area  = root.note.create('(?) %s...' % title[:15])
        title = 'Question Title: %s\n' % title


        markdown = question['body_markdown']
        markdown = '%s\n\n' % html.unescape(markdown)

        owner = question['owner']['display_name']
        owner = 'Question Owner: %s\n' % owner

        area.append(owner, '(YSX-OWNER)')
        area.append(title, '(YSX-TITLE)')
        area.append(markdown, '(YSX-DESC)')

        answers   = question.get('answers', ())
        qcomments = question.get('comments', ())

        for ind in qcomments:
            self.insert_qcomment(area, ind)

        for ind in answers:
            self.insert_answer(area, ind)

    def get_question(self, question_id):
        URL = 'https://api.stackexchange.com/2.2/questions/%s?/%s'
    
        params = {'order': 'desc', 'sort': 'activity', 'site': 'stackoverflow', 
        'filter': '!187D_k.dW21CE4wnVmvCCHjNi1rEqE0P7SF3wsJUVl*oQQ8(zCjIIa2yLgA_jn'}
    
        url = URL % (question_id, urlencode(params))
        req = requests.get(url)
        return json.loads(req.text)

    def insert_answer(self, area, answer):
        markdown = answer.get('body_markdown')
        markdown = '%s\n\n' % html.unescape(markdown)
        owner    = answer.get('owner')
        owner    = owner.get('display_name')
        owner    = '\nAnswer Owner: %s\n' % owner

        area.append(owner, '(YSX-OWNER)')
        area.append(markdown, '(YSX-DESC)')

        ecomments = answer.get('comments', [])

        for ind in ecomments:
            self.insert_ecomment(area, ind)

    def insert_ecomment(self, area, comment):
        markdown = comment.get('body_markdown')
        markdown = '%s\n\n' % html.unescape(markdown)
        owner    = comment.get('owner')
        owner    = owner.get('display_name')
        owner    = 'Comment Owner: %s\n' % owner

        area.append(owner, '(YSX-OWNER)')
        area.append(markdown, '(YSX-DESC)')

    def insert_qcomment(self, area, comment):
        markdown = comment.get('body_markdown')
        markdown = '%s\n\n' % html.unescape(markdown)
        owner    = comment.get('owner')
        owner    = owner.get('display_name')
        owner    = 'Comment Owner: %s\n' % owner

        area.append(owner, '(YSX-OWNER)')
        area.append(markdown, '(YSX-DESC)')

install = StackSOS
