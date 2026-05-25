import os
import json
import base64
from google import genai
from google.genai import types
from PIL import Image

def translate(request_type,image_input):

	if request_type == "translate":
		prompt = "Translate words in the image that are diffrent from english, if there are none or no image is found output the text 'none'"

		instruction = "You are a professional language traslator, when formating the answer, output the name of the translated text, then one newline, if the translated text is more than 100 words ignore the rest of this text, otherwise output this text 'Description:', then give a summarized background of traslated text"

		result = searchprompt(prompt, instruction, image_input)
		return result

	else:
		prompt = "What is the name of the main subject in the image. If subject isn't a landmark then output 'Only physical sites accepted'"

		instruction = "You are a professional Tour Guide, when formating the answer, output the name of the main subject in the image, then one newline, then location of the main subject, then a brief historical background of the main subject. One newline the text 'Similar: ' then another similar item loacated within near to the place"

		result = searchprompt(prompt, instruction, image_input)
		return result



client = genai.Client(api_key=os.environ.get("TRAVEL_WEBSITE"))

def searchprompt(prompt, instruction, image_input):

	image = Image.open(image_input)

	chat = client.chats.create(
		model="gemma-4-31b-it",
		config=types.GenerateContentConfig(
			system_instruction=instruction,
			max_output_tokens=1000,
		)
	)

	response = chat.send_message([image, prompt])

	chat_history = chat.get_history()

	chats = []

	for item in chat_history:
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

	with open("session.json", "w") as file:
		json.dump(chats, file)

	return response.text



def answerQuestion(prompt):

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

	chat = client.chats.create(
		model="gemma-4-31b-it",
		config=types.GenerateContentConfig(
			system_instruction="output only the answer and use history to refer in relation to the questions",
			max_output_tokens=1000,
		),
		history=prompt_types
	)

	response = chat.send_message(prompt)

	chat_history = chat.get_history()

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

	with open("session.json", "w") as file:
		json.dump(session_data, file, indent=4)

	return response.text

class sessionError(Exception):
	pass

def retrieveChats():

	with open("session.json", "r") as file:
		session_chats = json.load(file)

	text = []

	images_list = []

	chats = 0

	chats_list = []

	for data in session_chats:
		if  data["role"] == "user" and "image" in data["parts"]:
			#text = []
			#chats = 0

			text.append({data["role"]:f"{data["parts"]["text"]}"})
			image_data = {"image_data": f"data:{data["parts"]["image"][1]};base64,{data["parts"]["image"][0]}"}
			images_list.append(image_data)

			if len(chats_list) < 1 and chats == 0:
				chats += 1
			else:

			#if len(chats_list) > 1 and chats != 0:
				#chats += 1
				chats_list.append(chats)
				chats = 0
				chats += 1

		else:
			text.append({data["role"]:f"{data["parts"]["text"]}"})
			chats += 1

			if data == data[-1]:
				chats_list.append(chats)

	return images_list, text, chats_list