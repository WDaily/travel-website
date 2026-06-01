from external.agent import searchprompt, answerQuestion, recommendOutput
#from repository.database import createChat, readChat, readChats, updateChats
import base64
import json
import uuid

def translate(request_type,image_input):

	if request_type == "translate":
		prompt = "Translate words in the image that are diffrent from english, if there are none or no image is found output the text 'none'"

		instruction = "You are a professional language traslator, when formating the answer, output the name of the translated text, then one newline, if the translated text is more than 100 words ignore the rest of this text, otherwise output this text 'Description:', then give a summarized background of traslated text"

		result, chats = searchprompt(prompt, instruction, image_input)

		arranged = arrangeItems(chats)

		#to db
		#user_session = str(uuid.uuid4())
		#user_id = createChat(user_session, arranged)

		#user_sessions = [str(user_id) , user_session]

		with open("session.json", "w") as file:
			json.dump(arranged, file)

		return result #, user_sessions

	else:
		prompt = "What is the name of the main subject in the image. If subject isn't a landmark then output 'Only physical sites accepted'"

		instruction = "You are a professional Tour Guide, when formating the answer, output the name of the main subject in the image, then one newline, then location of the main subject, then a brief historical background of the main subject. One newline the text 'Similar: ' then another similar item loacated within near to the place"

		result, chats = searchprompt(prompt, instruction, image_input)
		

		arranged = arrangeItems(chats)

		#to db
		#user_session = str(uuid.uuid4())
		#user_id = createChat(user_session, arranged)

		#user_sessions = [str(user_id) , user_session]

		with open("session.json", "w") as file:
			json.dump(arranged, file)
			
		return result #, user_sessions

def arrengeItems(items):
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

def Questionscontrols(prompt): #user_sessions

	#obtain the items from db
	# session_data = readChat(user_sessions[0])

	with open("session.json", "r") as file:
		session_data = json.load(file)


	if not session_data:
		raise sessionError("no image uploaded and type selected")

		#prompt_types = []
	for sd in session_data:
		if sd["role"] == "user" and "image" in sd["parts"]:

			prompt_types = []
			image_bytes = base64.b64decode(sd["parts"]["image"][0])

			print(sd["role"])

			prompt_types.append(
				types.Content(
					role=sd["role"],
					parts=[
						types.Part.from_bytes(data=image_bytes, mime_type=sd["parts"]["image"][1]),
						types.Part.from_text(text=sd["parts"]["text"])
					]
				)
			)

		else:
			prompt_types.append(
				types.Content(
					role=sd["role"],
					parts=[
						types.Part.from_text(text=sd["parts"]["text"])
					]
				) 
			)

	response, chat_history = answerQuestion(prompt_types)

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

	#update
	#updateChats(session_data, user_sessions[0])

	with open("session.json", "w") as file:
		json.dump(session_data, file, indent=4)

	return response

class sessionError(Exception):
	pass

def retrieveChats(): #user_sessions

	#session_chats = readChats(user_sessions[1])

	with open("session.json", "r") as file:
		session_chats = json.load(file)

	text = []
	images_list = []
	chats = 0
	chats_list = []
	last_index = len(session_chats) - 1

	for index, data in enumerate(session_chats):
		if data["role"] == "user" and "image" in data["parts"]:

			text.append({data["role"]:f"{data['parts']['text']}"})
			images_list.append({"image_data": f"data:{data['parts']['image'][1]};base64,{data['parts']['image'][0]}"})

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