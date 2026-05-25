from external.agent import translate, answerQuestion, retrieveChats
from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)

app.secret_key = ("secret key")
#api_key=os.environ.get("SECRET_KEY")
CORS(app, supports_credentials=True)

@app.route('/translate', methods=['POST'])
def translate_text():


	if "image" not in request.files or "type" not in request.form:
		return jsonify({"status":"error", "message": "image or 'type' field missing"}), 400

	request_type =  request.form['type']
	image_file = request.files['image']

	request_type =  request.form.get('type')
	file = request.files.get('image')

	try:
		response = translate(request_type, image_file)

		return jsonify({"status":"success","response":response}), 200

	except Exception as e:
		return jsonify({"status":"error","message": str(e)}), 500


@app.route('/question', methods=['POST'])
def question():
	req = request.get_json()

	if not req or "question" not in req:
		return jsonify({"status":"error", "message":"Missing request or Missing 'question' field "}), 400

	quest = req.get('question')

	try:
		response = answerQuestion(quest)
		return jsonify({"status":"success", "response": response}), 200

	except Exception as e:
		return jsonify({"status":"error","message": f"Error Occured: {str(e)}"}), 500


@app.route('/reset', methods=['POST'])
def reset():

	session.pop("chat_history", None)

	return jsonify({"status":"success"}),200

@app.route("/chats", methods=["GET"])
def retrieve():

	try:
		images_list, text, chats_list = retrieveChats()
		return jsonify({"status":"success", "images":images_list, "chat":text,"amount":chats_list}), 200

	except Exception as e:
		return jsonify({"status":"error","message": str(e)}), 500


if __name__ == "__main__":
	app.run(debug=True, port=8080)