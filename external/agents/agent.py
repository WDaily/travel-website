import os
#import json
#import base64
from google import genai
from google.genai import types
from PIL import Image

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

	return response.text, chat_history

def answerQuestion(prompt):

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

	return response.text, chat_history

def recommendOutput(location, area, activity):

	#that starts with pictures if there are any and may also be embeded in the text. the images should have the following structure  "<img src='data:<image type>;base64,<image in bytes>' alt='upload preview' class='image-preview'/>". 

	prompt = f"name one recommendations with atleast one photo each of {activity} that are in a {area} radius form point {location}"

	instruction = """Display a summarized output of each. Before output of the text contained in quotations in the rest of this instuctions skip a line. Starting with the text "<b>Name: </b>" then the name of the place,"<b>Distance: </b>" then the approximate walking or driving distance from the given point, "<b>Experience: <b>" the backgrond history of the place while also including the experience and "<b>What others say:<b>" then what customers are saying."""

	#places = os.environ.get("PLACES-API")

	response = client.models.generate_content(
		model="gemma-4-31b-it",
		contents=prompt,
		config=types.GenerateContentConfig(
			system_instruction=instruction,
			max_output_tokens=1000,
		)
	)

	print("requested")

	return response.text