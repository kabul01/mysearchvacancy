import os, sys
import datetime


from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django
django.setup()

from app.parsers import hru
from app.models import Vacancy, Error, Url

User = get_user_model()

parsers = (
    (hru, 'hru'),


)


jobs, errors = [], []
def get_settings():
    #получаем набор уникальных значений города и языка
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)#получаем уникальные айдишки
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}#получаем весь набор что в базе данных
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            tmp['url_data'] = url_dict[pair]
            urls.append(tmp)
    return urls


# async def main(value):
#     func, url, city, language = value
#     job, err = await loop.run_in_executor(None, func, url, city, language)
#     errors.extend(err)
#     jobs.extend(job)

settings = get_settings()
url_list = get_urls(settings)

# loop = asyncio.get_event_loop()
# tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
#              for data in url_list
#              for func, key in parsers]



# if tmp_tasks:
#     tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
#     loop.run_until_complete(tasks)
#     loop.close()


for data in url_list:
    for func,key in parsers:
        url = data['url_data'][key]
        j,e = func(url, city=data['city'], language=data['language'])
        jobs += j
        errors += e



for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass


if errors:
    er = Error(data=errors).save()

# if errors:
#     qs = Error.objects.filter(timestamp=datetime.date.today())
#     if qs.exists():
#         err = qs.first()
#         err.data.update({'errors': errors})
#         err.save()
#     else:
#         er = Error(data=f'errors:{errors}').save()



# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
