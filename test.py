import random
import json
import torch
from NeuralNetwork import Model
import re
from nplPipeline import bag_of_words, tokenize
import requests

def get_def(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url)
    worddict = response.json()
    return worddict[0]['meanings'][0]['definitions'][0]['definition']

print(get_def('goodbye'))


# weatherAPI = '3f465ec287cfeb5fa02a21445f57f65b'

# def get_weather(city):
#     url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherAPI}'
#     response = requests.get(url)
#     return response.json()

# def get_response(sentence):
#     text = sentence
#     sentence = tokenize(sentence)
#     bag = bag_of_words(sentence, all_words)
#     bag = bag.reshape(1, bag.shape[0])
#     bag = torch.from_numpy(bag).float()
    
#     output = model(bag)
    
#     _, predicted = torch.max(output, dim=1)
#     tag = tags[predicted.item()]
    
#     probs = torch.softmax(output, dim=1)
#     probability = probs[0][predicted.item()]
    
#     return probability.item()

# city = 'Houston'
# sentence = "What is the weather in Houston?"

# print(get_weather(city))
# print(f'The current temperature in {city} is {round((get_weather(city)["main"]["temp"]-273.15) * (9/5) + 32)}°F with {get_weather(city)["weather"][0]["description"]}.')

# data = torch.load("model.pth")

# input_size = data["input_size"]
# hidden_size = data["hidden_size"]
# output_size = data["output_size"]
# all_words = data["all_words"]
# tags = data["tags"]
# model_state = data["model_state"]

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model = Model(input_size, hidden_size, output_size).to(device)

# sentence = "How are you?"

# print(get_response(sentence))