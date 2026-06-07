import os
import base64
from google import genai
from google.genai import types
from PIL import Image
import io

client = genai.Client(api_key=os.environ.get("TRAVEL_WEBSITE"))

def searchprompt(prompt, instruction, image_input):

	image = Image.open(image_input)

	image.thumbnail((384, 384))

	buffer = io.BytesIO()

	image.save(buffer, format="JPEG", quality=85)

	image_buffer = buffer.getvalue()

	image_structure =types.Part.from_bytes(
		data=image_buffer,
		mime_type="image/jpeg"
	)

	chat = client.chats.create(
		model="gemma-4-31b-it",
		config=types.GenerateContentConfig(
			system_instruction=instruction,
			max_output_tokens=850,
			media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW,
			temperature=0.1
		)
	)
	response = chat.send_message([image_structure, prompt])

	chat_history = chat.get_history()

	return response.text, chat_history

def answerQuestion(prompt, session_data):

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
			system_instruction="output only the answer, use history as a reference to answer the questions and provide your answer in plain text only.",
			max_output_tokens=1000,
			temperature=0.1
		),
		history=prompt_types
	)

	response = chat.send_message(prompt)

	chat_history = chat.get_history()

	return response.text, chat_history

def recommendOutput(location, area, activity):

	prompt = f"name two recommendations of {activity} that are in a {area} radius form point {location}"
	instruction = "Display a summarized output fast of each in text only. when formating the answer, output the name of the place, then output this '\n', output this text 'Distance:' then the approximate walking or driving distance from the given point to the recommended area, then output this '\n', output this text Experience:' the backgrond history of the place while also including the experience, then output this '\n', output this text 'What others say:' then what customers are saying about the place, then output this '\n\n'"

	response = client.models.generate_content(
		model="gemma-4-31b-it",
		contents=prompt,
		config=types.GenerateContentConfig(
			system_instruction=instruction,
			max_output_tokens=1000,
			temperature=0.1
		)
	)

	return response.text