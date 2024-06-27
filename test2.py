# import requests
# import os

# os.system('cls')

# stockAPI = '477c206ae68c40dda2f70e9d696193ba'
# symbol = 'VGT'
# interval = '1day'

# url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={stockAPI}'

# response = requests.get(url)
# stockInfo = response.json()
# # print(stockInfo)

# stockName = stockInfo['meta']['symbol']
# stockPrice = float(stockInfo['values'][0]['open'])
# stockHigh = float(stockInfo['values'][0]['high'])
# stockLow = float(stockInfo['values'][0]['low'])
# stockTrend = float(stockInfo['values'][20]['open'])
# # print(stockTrend)
# print(f'Stock Name: {stockName}. Stock Current Price: ${stockPrice:.2f} Stock Low Price: ${stockLow:.2f} Stock High Price: ${stockHigh:.2f}')

# print(f'A month ago, {stockName} was worth ${stockTrend:.2f}, today it is worth ${stockPrice:.2f}, a {(((stockPrice-stockTrend)/stockTrend)*100):.2f}% change')
import random

def get_random_quote():
    with open('quotes.csv', 'r') as f:
        lines = f.readlines()
        f.close()
    newlines = []
    for line in lines:
        newline = line.split(';')
        newlines.append(newline)
        
    randQuote = random.randint(0,len(newlines)-1)
        
    print(f'{newlines[randQuote][1]}- {newlines[randQuote][0][1:-1]}')
    
get_random_quote()
    