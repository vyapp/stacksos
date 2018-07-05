tee >(stdbuf -o 0 python -i)

import requests
import json

url = 'https://api.stackexchange.com/2.2/questions/18474564?order=desc&sort=activity&site=stackoverflow&filter=!9YdnSJ*_T'

req = requests.get(url)
data = json.loads(req.text)
data

url = 'https://www.google.com.br'
req = requests.get(url)

fd = open('foo.html', 'w')
fd.write(req.text)
fd.close()
req.text
URL_HOME = 'https://www.google.com'
req = requests.get(URL_HOME)

jar = requests.cookies.RequestsCookieJar()
req.cookies.items()

from urllib.parse import urlencode

url_search = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
             "btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&tbm=%(tpe)s"

def search(data, params={'tld':'com', 'hl':'en', 
    'tbs':'0', 'safe':'off', 'tpe':''}):
    URL_HOME = 'https://www.google.com'
    req = requests.get(URL_HOME)
    params['q'] = data
    url ='https://www.google.com/search?%s' % urlencode(params)
    req = requests.get(url, cookies=req.cookies)
    return req

req = search('stackoverflow api')
req.text
fd = open('foo.html', 'w')
fd.write(req.text)
fd.close()

import requests
from vyapp.ask import Ask, Get
from vyapp.app import root
import lxml.html

class Google:
    URL_HOME   = 'https://www.google.com'
    URL_SEARCH = 'https://www.google.com/search?%s'
    def __init__(self, params={'tld':'com', 'hl':'en', 
        'tbs':'0', 'safe':'off', 'tpe':''}):
        self.params = params
    def search(self, data):
        req = requests.get(self.URL_HOME)
        self.params['q'] = data
        url =self.URL_SEARCH % urlencode(self.params)
        req = requests.get(url, cookies=req.cookies)
        return req

    def build(self, data):
        dom   = lxml.html.fromstring(data)
        elems = dom.xpath("//div[@class='rc']")
        for ind in elems:
            yield {
                'title': ind.xpath(".//h3[@class='r']").text, 
                'desc': ind.xpath(".//span[@class='st']").text, 
                'url': ind.xpath(".//h3[@class='r']").text
            }


x = Google()
req = x.search('lxml python')
req.text
from urllib.parse import parse_qs, parse_qsl
q = parse_qs('/url?q=http://www.gurobi.com/documentation/8.0/examples/python_examples.html&sa=U&ved=0ahUKEwj6pfL8-4TcAhXCiJAKHflICRIQFghIMAg&usg=AOvVaw0lZaaP7vfd6PBOuPnerBgq')
q
q['/url?q']

data = "test=test&test2=test2&test2=test3"
q = parse_qs(data)
q

##############################################################################
from urllib.parse import urlencode
import requests
import json
url = 'https://api.stackexchange.com/2.2/questions/18474564?order=desc&sort=activity&site=stackoverflow&filter=!9YdnSJ*_T'


def question(id, order='desc', sort='activity', answers='true',
    site='stackoverflow', filter='!9YdnSJ*_T'):
    params = {'order': order, 'sort': sort, 'answers': answers,
    'site': site, 'filter': filter}
    STACK_URL = 'https://api.stackexchange.com/2.2/questions/%s?/%s'
    url = STACK_URL % (id, urlencode(params))
    print(url)
    req = requests.get(url)
    return json.loads(req.text)


question(18474564,)


from gle import Google
import time
# Count is the number of pages that you want to extract results.
x = Google(count=3)
pages = x.search('stackoverflow python vy editor')

for indi in pages:
    for indj in indi:
        print(indj)

from urllib.parse import urlencode
import requests
import json

def get_answer_data(question_id, order='desc', sort='activity', 
    site='stackoverflow', filter='!9YdnSJ*_T'):
    STACK_URL = 'https://api.stackexchange.com/2.2/questions/%s/answers?%s'
    params = {'order': order, 'sort': sort, 
    'site': site, 'filter': filter}
    url = STACK_URL % (question_id, urlencode(params))
    req = requests.get(url)
    return json.loads(req.text)



def get_answers(question_id, order='desc', sort='activity', 
    site='stackoverflow', filter='!2uDdBASlzGE6U5lW)pVBlUm5WP0s37p*nnpd1zxfWA'):
    STACK_URL = 'https://api.stackexchange.com/2.2/questions/%s/answers?%s'
    params = {'order': order, 'sort': sort, 
    'site': site, 'filter': filter}
    url = STACK_URL % (question_id, urlencode(params))
    print('the answers url', url)
    req = requests.get(url)
    return json.loads(req.text)

q = get_answers(20921619, filter='!WyX5UezTc0C3EZPZ*F2m.(TE3yxC7yJisQjzoZj')
q['items'][0]['title']


def get_answers(question_id, order='desc', sort='activity', 
    site='stackoverflow', filter='!WyX5UezTc0C3EZPZ*F2m.(TE3yxC7yJisQjzoZj'):
    STACK_URL = 'https://api.stackexchange.com/2.2/questions/%s/answers?%s'
    params = {'order': order, 'sort': sort, 
    'site': site, 'filter': filter}
    url = STACK_URL % (question_id, urlencode(params))
    req = requests.get(url)
    return json.loads(req.text)

q = get_answers(19208725)
q['items']
q['items'][0]['title']

def get_question(id, order='desc', sort='activity', 
    site='stackoverflow', filter='!WyX5UezTc0C3EZPZ*F2m.(TE3yxC7yJisQjzoZj'):
    STACK_URL = 'https://api.stackexchange.com/2.2/questions/%s?/%s'
    params = {'order': order, 'sort': sort, 
    'site': site, 'filter': filter}
    url = STACK_URL % (id, urlencode(params))
    req = requests.get(url)
    return json.loads(req.text)

q = get_question(35977862)
q['items']

import re
url='https://stackoverflow.com/questions/19208725/example-for-sync-waitgroup-correct'
url = 'https://stackoverflow.com/a/35554720'

mch = re.search('q[uestion]/([0-9]+)/?', url)
mch.group(1)


