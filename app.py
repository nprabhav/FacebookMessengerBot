from flask import Flask, request
from pymessenger import Bot
from utils import wit_response,get_news_elements

app = Flask("My echo bot")

fb_token = "EAAEWc3Uylh0BADtOoZCKan98hEVZBY9H7Lbr9wpZBXkuFtX8siwcCiGN5q7tf0bVpUxDZB7Q6QComD0ZCsZBbpjQmqZCkAYKbuBSbTW63KPViXunnVfi9NZAuF1cgR3mgFZCi3pKmAeooLWFOlMZB3ZAGlEDiDmj3QjoTrPDcHtIdZBqZCAZDZD"
bot = Bot(fb_token)

v_token = "hello"


@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == v_token:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	print(request.data),
	data = request.get_json()

	if data['object'] == "page":
		entries = data['entry']

		for entry in entries:
			messaging = entry['messaging']

			for messaging_event in messaging:

				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# normal messages
					if messaging_event['message'].get('text'):
						# text msg
						query = messaging_event['message']['text']

						categories = wit_response(query)
						#print(categories)
						elements = get_news_elements(categories)
						#print(elements)


						# print(query)
						# response = None
						# entity,value = wit_response(query)
						#
						# if entity == "newstype":
						# 	response = "Okay, I will send you {} news".format(str(value))
						# elif entity == "location":
						# 	response = "Okay, so you live in {0}. I will send you top headlines from {0}".format(str(value))
						#
						# if response == None:
						# 	response = "Sorry, I didn't understand!"
						# bot.send_text_message(sender_id,"Hi")
						if(elements):
							print("------------------------------------------------------")
							print(elements)
							print("------------------------------------------------------")
						try:
							bot.send_text_message(sender_id,elements[0]['title'])
						# 	#print(bot.send_generic_message(sender_id, elements))
						except:
						# 	#print(bot.send_text_message(sender_id,"Not found"))
							bot.send_text_message(sender_id,"Not found")

						# bot.send_generic_message(recipient_id, elements)
	return "ok", 200


if __name__ == "__main__":
	app.run(port=8010, use_reloader = True)
