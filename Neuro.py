import random
import json
import torch
from NeuralNetwork import Model
import re
from nplPipeline import bag_of_words, tokenize
import requests
import webbrowser
import datetime
import os

os.system('cls')

weatherAPI = '3f465ec287cfeb5fa02a21445f57f65b'
stockAPI = '477c206ae68c40dda2f70e9d696193ba'
interval = '1day'
bot_name = "Neuro"
convo = True
musicLinks = ["https://www.youtube.com/watch?v=gpnQhbOMQDA", "https://youtu.be/h35g2e9aIIk", "https://youtu.be/Eyt40gCbYeU", "https://youtu.be/bICi2mKwmpA", "https://youtu.be/cLx87ceoNT8"]

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherAPI}'
    response = requests.get(url)
    return response.json()

def get_stocks(symbol):
    url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={stockAPI}'
    response = requests.get(url)
    return response.json()

def get_def(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url)
    worddict = response.json()
    return worddict[0]['meanings'][0]['definitions'][0]['definition']

def get_random_quote():
    with open('quotes.csv', 'r') as f:
        lines = f.readlines()
        f.close()
    newlines = []
    for line in lines:
        newline = line.split(';')
        newlines.append(newline)
        
    randQuote = random.randint(0,len(newlines)-1)
        
    return f'{newlines[randQuote][1]}- {newlines[randQuote][0][1:-1]}'

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
    # tag_predictions = []
    # for i, prob in enumerate(probs[0]):
    #     tag_predictions.append((tags[i], prob.item()))
    # print(tag_predictions)
    probability = probs[0][predicted.item()]
    print(probability.item())
    
    if probability.item() > 0.85:
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
                            return f'A month ago, {stock} was worth ${float(get_stocks(stock)["values"][20]["open"]):.2f}, today it is worth ${float(get_stocks(stock)["values"][0]["open"]):.2f}, a {(((float(get_stocks(stock)["values"][0]["open"])-float(get_stocks(stock)["values"][20]["open"]))/float(get_stocks(stock)["values"][20]["open"]))*100):.2f}% change'
                    if not stockFound:
                        return f'Could not find stock trend'
            if tag == 'dictionary':
                with open('words.txt', 'r') as f:
                    wordLst = f.readlines()
                    wordFound = False
                    for word in wordLst:
                        word = word[:-1]
                        if word in text:
                            return f'The word {word} means {get_def(word)}'
                    if not wordFound:
                        return f'Could not find word'
            if tag == 'time':
                with open('list.txt', 'r') as f:
                    cityLst = f.readlines()
                    cityFound = False
                    for city in cityLst:
                        city = city[:-1]
                        # print(city)
                        if city in text:
                            # print(city)
                            return f'The current time in {city} is {(datetime.datetime.utcfromtimestamp(get_weather(city)["dt"]+get_weather(city)["timezone"])).strftime("%I:%M %p")}.'
                    if not cityFound:
                        return "Please provide a city."
            if tag == 'quote':
                return get_random_quote()
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