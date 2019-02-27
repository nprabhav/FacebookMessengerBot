import os
import apiai
import json
import requests
from pymongo import MongoClient
from gnewsclient import gnewsclient


############################  MONGODB INTEGRATION #################################

# # mongoDB client
# MONGODB_URI = os.environ.get("MONGODB_URI")
# client = MongoClient(MONGODB_URI, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True)
# db = client.get_default_database()
# news_records = db.news_records
#
# def getRECORDS(user_id):
# 	"""
# 	function to fetch all news searches of a user
# 	"""
# 	records = news_records.find({"sender_id":user_id})
# 	return records
#
# def pushRECORD(record):
# 	"""
# 	function to push news record to collection
# 	"""
# 	news_records.insert_one(record)

####################################################################################

# api.ai client
# APIAI_ACCESS_TOKEN = os.environ.get("APIAI_ACCESS_TOKEN")
APIAI_ACCESS_TOKEN = "ecc6a68948ae4c4c8114a7e2d668c36c"
ai = apiai.ApiAI(APIAI_ACCESS_TOKEN)

# endpoint of the news API
GNEWS_API_ENDPOINT = "https://gnewsapi.herokuapp.com"

# available news categories
news_categories = [('sports', 'sports news'), ('political', 'political news'), ('business', 'business news'),
				   ('top stories', 'top stories news'), ('world', 'world news'), ('national', 'national news'),
					('technology', 'technology news'), ('entertainment', 'entertainment news')]

# a help message
HELP_MSG = """
Hey! I am NewsBot.
I can provide you news from all around the world in different languages, on different topics!
Try any of these categories. :)
"""



def get_news(params):
	"""
	function to fetch news from news API
	"""
	params['news'] = params.get('news_type', "top stories")
	#resp = requests.get(GNEWS_API_ENDPOINT, params = params)

	return resp.json()

'''
edited
'''
def get_news_elements(categories):
    news_client = gnewsclient()
    news_client.query = ''

    if categories['newstype'] != None:
        news_client.query += str(categories['newstype']) + ' '

    if categories['location'] != None:
        news_client.query += str(categories['location'])

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
    return news_items
'''
'''
def apiai_response(query, session_id):
	"""
	function to fetch api.ai response
	"""
	request = ai.text_request()
	print("Request  :  ")
	print(request)
	request.lang='en'
	request.session_id=session_id
	request.query = query
	response = request.getresponse()
	return json.loads(response.read().decode('utf8'))


def parse_response(response):
	"""
	function to parse response and
	return intent and its parameters
	"""
	result = response['result']
	params = result.get('parameters')
	intent = result['metadata'].get('intentName')
	return intent, params


def fetch_reply(query, session_id):
	"""
	main function to fetch reply for chatbot and
	return a reply dict with reply 'type' and 'data'
	"""
	response = apiai_response(query, session_id)
	print("Response :")
	print(response)
	intent, params = parse_response(response)

	reply = {}
	print("Intent :")
	print(intent)
	print("Params` :")
	print(params)
	if response['result']['action'].startswith('smalltalk'):
		reply['type'] = 'smalltalk'
		reply['data'] = response['result']['fulfillment']['speech']

	elif intent == None:
		reply['type'] = 'none'
		reply['data'] = [{"type":"postback",
						  "payload": "SHOW_HELP",
						  "title":"Click here for help!"}]
		# print("Reply2 :")
		# print(reply)
	elif intent == "news":
		reply['type'] = 'news'
		params['sender_id'] = session_id

		# push news search record to mongoDB
		# pushRECORD(params)
		# print("Reply3 :")
		# print(reply)
		articles = get_news_elements(params)
		# print
		# print("Articles :")
		# print(articles)
		# create generic template
		news_elements = []

		for article in articles[:10]:
			element = {}
			element['title'] = article['title']
			element['item_url'] = article['link']
			element['image_url'] = article['img']
			element['buttons'] = [{
				"type":"web_url",
				"title":"Read more",
				"url":article['link']}]
			news_elements.append(element)

		reply['data'] = news_elements
	elif intent == "Default Welcome Intent":
		reply['type'] = 'welcome'
		reply['data'] = response['result']['fulfillment']['speech']
	elif intent == "Default Fallback Intent":
		reply['type'] = 'fallback'
		reply['data'] = response['result']['fulfillment']['speech']
	elif intent == "help":
		reply['type'] = 'help'
	# print(reply)
	return reply
