from flask import Flask, request
from pymessenger import Bot

app = Flask("My echo bot")

fb_token = "EAAKHYGtwONoBAPQvTmPtZBXWKis8YGMz96XbDuNZCrMN6vkGhFEPVZCeKGIZBwXlLKv4jHHXAAErMG5kZB299bqBlD4j23OYzpIBqriowCgg6Qs45obLmZAAqtAKcOhBJAynqr5JSzg0itvItrZCPAkyaQr2SukQU3PtVmZBpAyJ4QZDZD"
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
	app.run(port=8010, use_reloader = True)
#https://88aa4d39.ngrok.io/
