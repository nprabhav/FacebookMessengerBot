from wit import Wit
from gnewsclient import gnewsclient
import os
import sys
import json


access_token = "6G7FK2N4BL3ZRSH2VZQRZ4D65RMBTIZX"
client = Wit(access_token = access_token)

def wit_response(message_text):
    resp =  client.message(message_text)
    categories = {'newstype': None, 'location': None}

    entities = list(resp['entities'])
    for entity in entities:
        categories[entity] = resp['entities'][entity][0]['value']

    return categories

def get_news_elements(categories):
    news_client = gnewsclient()
    news_client.query = ''

    if categories['newstype'] != None:
        news_client.query += categories['newstype'] + ' '

    if categories['location'] != None:
        news_client.query += categories['location']

    news_items = news_client.get_news()
    elements = []
    #print(news_items)
    if news_items:
        for item in news_items[0:5]:
            element = {
                        'title': item['title'],
                        'buttons': [{
                                        'type': 'web-url',
                                        'title': "Read more",
                                        'url': "NoneLOLNone"
                        }],
                        'image_url': item['img']
            }
            elements.append(element)
    #print(elements)
    return elements
#print(get_news_elements(wit_response("I want sport news")))
