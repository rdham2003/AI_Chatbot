import random
import json
import torch
from NeuralNetwork import Model
import re
from nplPipeline import bag_of_words, tokenize
import requests

weatherAPI = '3f465ec287cfeb5fa02a21445f57f65b'
bot_name = "Neuro"
convo = True

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherAPI}'
    response = requests.get(url)
    return response.json()

def get_response(sentence):
    text = sentence
    sentence = tokenize(sentence)
    bag = bag_of_words(sentence, all_words)
    bag = bag.reshape(1, bag.shape[0])
    bag = torch.from_numpy(bag).float()
    
    output = model(bag)
    
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    
    probs = torch.softmax(output, dim=1)
    # print(probs)
    probability = probs[0][predicted.item()]
    # print(probability.item())
    
    if probability.item() > 0.75:
      for intent in intents["intents"]:
        if tag == intent["tag"]:
            response = f'{random.choice(intent["responses"])}'
            if tag == 'math':
                expression = re.findall(r'\d+\.?\d*|[+\-*/]', text)
                if expression:
                    try:
                        result = eval(" ".join(expression))
                        return f"The result is {result}"
                    except Exception as e:
                        return "Sorry, I couldn't solve that math problem."
                else:
                    return "Please provide a valid math expression."
            if tag == 'weather':
                with open('list.txt', 'r') as f:
                    cityLst = f.readlines()
                    cityFound = False
                    for city in cityLst:
                        city = city[:-1]
                        # print(city)
                        if city in text:
                            # print(city)
                            return f'The current temperature in {city} is {round((get_weather(city)["main"]["temp"]-273.15) * (9/5) + 32)}°F with {get_weather(city)["weather"][0]["description"]}.'
                    if not cityFound:
                        return "Could no locate city."
            if tag == 'farewell':
                global convo
                convo = False
                return response
            else:
                return response
    else:
        return f'Sorry, I do not understand...'

with open("intents.json", 'r') as tData:
    intents = json.load(tData)
    
data = torch.load("model.pth")

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = Model(input_size, hidden_size, output_size).to('cpu')
model.load_state_dict(model_state)
model.eval()

print("Let's talk! (Type 'quit' to stop conversation)")    
while convo:
    sentence = input("You: ")
    print(f"{bot_name}: {get_response(sentence)}")