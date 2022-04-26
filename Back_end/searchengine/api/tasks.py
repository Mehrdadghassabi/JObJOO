from requests import post
from datetime import datetime
import json

from searchengine.celery import app


@app.task
def call_sheypoor_spider():
    url = "http://localhost:7000/schedule.json" #scrapy port in server is 7000
    try:
       response = post(url, data={
           'project': 'crawler',
           'spider': 'sheypoor',
           'category': 'recruitment'
       })
    except:
       return
    json_data = json.loads(response.content)

    print(json_data)

@app.task
def call_divar_spider():
    url = "http://localhost:7000/schedule.json" #scrapy port in server is 7000
    try:
       response = post(url, data={
           'project': 'crawler',
           'spider': 'divar',
           'category': 'jobs'
       })
    except:
       return
    json_data = json.loads(response.content)

    print(json_data)