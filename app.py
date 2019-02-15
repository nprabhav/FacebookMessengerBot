from flask import Flask, request
from pymessenger import Bot

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
	print(request.data)
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
						#echo
						bot.send_text_message(sender_id, query)
	return "ok", 200


if __name__ == "__main__":
	app.run(port=8000, use_reloader = True)
