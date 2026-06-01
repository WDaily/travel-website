from logic.logic import translate, QuestionControls, retrieveChats, recommendations
from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)

app.secret_key = "secret_key"

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
		response = translate(request_type, image_file) #returns user_sessions

		#session["user_sessions"] = user_sessions

		return jsonify({"status":"success","response":response}), 200

	except Exception as e:
		return jsonify({"status":"error","message": str(e)}), 500

@app.route('/question', methods=['POST'])
def question():
	req = request.get_json()

	if not req or "question" not in req:
		return jsonify({"status":"error", "message":"Missing request or Missing 'question' field "}), 400

	quest = req.get('question')

	#user_sessions = session.get("user_sessions", [])

	try:
		response = QuestionControls(quest) #also send user_sessions
		return jsonify({"status":"success", "response": response}), 200

	except Exception as e:
		return jsonify({"status":"error","message": f"Error Occured: {str(e)}"}), 500

@app.route('/reset', methods=['POST'])
def reset():

	session.pop("chat_history", None)

	return jsonify({"status":"success"}),200

@app.route("/chats", methods=["GET"])
def retrieve():

	#user_sessions = session.get("user_sessions", [])

	try:
		images_list, text, chats_list = retrieveChats() #also send user_sessions
		return jsonify({"status":"success", "images":images_list, "chat":text,"amount":chats_list}), 200

	except Exception as e:
		return jsonify({"status":"error","message": str(e)}), 500

@app.route("/recommend", methods=["POST"])
def recommend():
	req = request.get_json()

	if not req:
		return jsonify({"status":"error", "message":"Missing request"}), 400

	location = req.get('location') #coordinates
	area = req.get("area") #radius
	activity = req.get("activity") #eg hotel, parks, concerts, 

	try:
		text = recommendations(location, area, activity)
		return jsonify({"status": "success", "text":text}), 200

	except Exception as e:
		return jsonify({"status":"error", "message": str(e)}), 500

if __name__ == "__main__":
	app.run(debug=True, port=8080)