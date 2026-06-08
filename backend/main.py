from logic.logic import translate, QuestionsControls, retrieveChats, recommendations
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from hypercorn.middleware import ProxyFixMiddleware

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

CORS(app, supports_credentials=True) 

app.wsgi_app = ProxyFixMiddleware(app.wsgi_app, mode="legacy", trusted_hops=1)

app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_PARTITIONED"] = True


@app.route('/translate', methods=['POST'])
def translate_text():
	if "image" not in request.files or "type" not in request.form:
		return jsonify({"status":"error", "message": "image or 'type' field missing"}), 400

	request_type =  request.form['type']
	image_file = request.files['image']

	request_type =  request.form.get('type')
	file = request.files.get('image')

	user_sessions = session.get("user_sessions")

	try:
		response, sessions = translate(request_type, image_file, user_sessions)
		session["user_sessions"] = sessions
		return jsonify({"status":"success","response":response}), 200

	except Exception as e:
		return jsonify({"status":"error","message": str(e)}), 500

@app.route('/question', methods=['POST'])
def question():
	req = request.get_json()

	if not req or "question" not in req:
		return jsonify({"status":"error", "message":"Missing request or Missing 'question' field "}), 400

	quest = req.get('question')

	user_sessions = session.get("user_sessions", [])
	
	try:
		response = QuestionsControls(quest, user_sessions)
		return jsonify({"status":"success", "response": response}), 200

	except Exception as e:
		return jsonify({"status":"error","message": f"Error Occured: {str(e)}"}), 500

@app.route('/reset', methods=['POST'])
def reset():

	session.pop("chat_history", None)

	return jsonify({"status":"success"}),200

@app.route("/chats", methods=["GET"])
def retrieve():

	user_sessions = session.get("user_sessions", [])
	try:
		images_list, text, chats_list = retrieveChats(user_sessions)
		return jsonify({"status":"success", "images":images_list, "chat":text,"amount":chats_list}), 200

	except Exception as e:
		return jsonify({"status":"error","message": str(e)}), 500

@app.route("/recommend", methods=["POST"])
def recommend():
	req = request.get_json()

	if not req:
		return jsonify({"status":"error", "message":"Missing request"}), 400

	location = req.get('location')
	area = req.get("area")
	activity = req.get("activity") 

	try:
		text = recommendations(location, area, activity)
		return jsonify({"status": "success", "text":text}), 200

	except Exception as e:
		return jsonify({"status":"error", "message": str(e)}), 500