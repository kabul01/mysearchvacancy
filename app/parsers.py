import requests
import codecs
from random import randint

from bs4 import BeautifulSoup as BS
__all__=('hru')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def hru(url, city=None, language = None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='a11y-main-content')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
                for div in div_list:
                    title = div.find('h3')
                    href = title.a['href']
                    content = div.find('div', attrs={'class': 'g-user-content'})
                    company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
                    jobs.append({'title': title.text, 'url': href,
                                 'description': content.text, 'company': company.text,
                                 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div does not exists'})
        else:
            errors.append({'url': url, 'title': 'Page do not response'})

        return jobs, errors



