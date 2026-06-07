from external.agents.agent import searchprompt, answerQuestion, recommendOutput
from external.repository.database import createChat, readChat, readChats, updateChats
import base64
import json
import uuid
from PIL import Image
import io

def translate(request_type,image_input, sessions):

	if request_type == "translate":
		prompt = "Translate words in the image that are diffrent from english."
		instruction = "You are a professional language traslator, when formating the answer, output the name of the translated text, then one newline, output this text 'Description:', then give a summarized background of traslated text. if there nothing to translate or no image is found output the text 'none'"

		result, chats = searchprompt(prompt, instruction, image_input)
		arranged = arrangeItems(chats)

		if not sessions:
			user_session = str(uuid.uuid4())
			user_id = createChat(user_session, arranged)
			user_sessions = [user_session, user_id]

		else:
			user_id = createChat(sessions[0], arranged)
			user_sessions = sessions.append(user_id)

		return result, user_sessions

	else:
		prompt = "What is the name of the main subject in the image."
		instruction = "You are a professional Tour Guide, when formating the answer, output the name of the main subject in the image, then one newline, then location of the main subject, then a brief historical background of the main subject and a similar item loacated close to the place. If subject isn't a landmark then output 'Only physical sites accepted'"

		result, chats = searchprompt(prompt, instruction, image_input)
		arranged = arrangeItems(chats)

		if not sessions:
			user_session = str(uuid.uuid4())
			user_id = createChat(user_session, arranged)
			user_sessions = [user_session, user_id]

		else:
			print("sessions present")
			user_id = createChat(sessions[0], arranged)
			user_sessions = sessions.append(user_id)
			
		return result, user_sessions

def arrangeItems(items):
	chats = []

	for item in items:
		if item.role == "user":

			image_bytes = item.parts[0].inline_data.data

			image_string = base64.b64encode(image_bytes).decode("utf-8")

			chats.append({"role":item.role, 
				"parts":{
					"image":[image_string, item.parts[0].inline_data.mime_type],
					"text":item.parts[1].text
				}
			})
			
		else:

			chats.append({"role":item.role, 
				"parts":{
					"text":item.parts[1].text
				}
			})
	return chats

def QuestionsControls(prompt, user_sessions):

	user_id = user_sessions[-1]
	session_data = readChat(user_id)

	if not session_data:
		raise sessionError("no image uploaded and type selected")

	response, chat_history = answerQuestion(prompt, session_data)

	session_data.extend([ 
				{"role":chat_history[-2].role,
					"parts":{
						"text":chat_history[-2].parts[0].text
					}
				},
				{"role":chat_history[-1].role,
					"parts":{
						"text":chat_history[-1].parts[1].text
					}
				}
			])

	updateChats(session_data, user_id)

	return response

class sessionError(Exception):
	pass

def retrieveChats(user_sessions):
	print(f"sessions: {user_sessions[0]}")
	session_chats = readChats(user_sessions[0])

	text = []
	images_list = []
	chats = 0
	chats_list = []
	last_index = len(session_chats) - 1

	for index, data in enumerate(session_chats):
		if data["role"] == "user" and "image" in data["parts"]:

			image_bytes = base64.b64decode(data['parts']['image'][0])
			img = Image.open(io.BytesIO(image_bytes))
			
			img.thumbnail((200, 200))
			
			buffer = io.BytesIO()
			img.save(buffer, format="JPEG", quality=60)
			thumb_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

			text.append({data["role"]:f"{data['parts']['text']}"})
			images_list.append({"image_data": f"data:image/jpeg;base64,{thumb_b64}"})

			if len(chats_list) < 1 and chats == 0:
				chats += 1
			else:
				chats_list.append(chats)
				chats = 1

		else:
			text.append({data["role"]:f"{data['parts']['text']}"})
			chats += 1

			if index == last_index:
				chats_list.append(chats)

	return images_list, text, chats_list


def recommendations(location, area, activity):

	response = recommendOutput(location, area, activity)

	return response