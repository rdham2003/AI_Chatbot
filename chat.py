import random
import json
import torch
from NeuralNetwork import Model
import re
from nplPipeline import bag_of_words, tokenize
import requests
import webbrowser

weatherAPI = '3f465ec287cfeb5fa02a21445f57f65b'
stockAPI = '477c206ae68c40dda2f70e9d696193ba'
interval = '1day'
bot_name = "Neuro"
convo = True
musicLinks = ["https://www.youtube.com/watch?v=gpnQhbOMQDA", "https://youtu.be/h35g2e9aIIk", "https://youtu.be/Eyt40gCbYeU"]

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherAPI}'
    response = requests.get(url)
    return response.json()

def get_stocks(symbol):
    url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={stockAPI}'
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
    
    if probability.item() > 0.95:
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
            if tag == 'music':
                randomSong = random.randint(0,len(musicLinks)-1)
                webbrowser.open(musicLinks[randomSong])
                return "Just Listen"
            if tag == 'stocks_price':
                with open('nasdaq_tickers.txt', 'r') as f:
                    stockLst = f.readlines()
                    stockFound = False
                    for stock in stockLst:
                        stock = stock[:-1]
                        if stock in text:
                            return f'Stock Name: {stock}. Stock Current Price: ${float(get_stocks(stock)["values"][0]["open"]):.2f} Stock Low Price: ${float(get_stocks(stock)["values"][0]["low"]):.2f} Stock High Price: ${float(get_stocks(stock)["values"][0]["high"]):.2f}'
                    if not stockFound:
                        return f'Could not find stock'
            if tag == 'stocks_trend':
                with open('nasdaq_tickers.txt', 'r') as f:
                    stockLst = f.readlines()
                    stockFound = False
                    for stock in stockLst:
                        stock = stock[:-1]
                        if stock in text:
                            return f'Stock Name: {stock}. Stock Current Price: ${float(get_stocks(stock)["values"][0]["open"]):.2f} Stock Low Price: ${float(get_stocks(stock)["values"][0]["low"]):.2f} Stock High Price: ${float(get_stocks(stock)["values"][0]["high"]):.2f}'
                    if not stockFound:
                        return f'Could not find stock trend'
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