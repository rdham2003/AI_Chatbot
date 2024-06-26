import requests
import os

os.system('cls')

stockAPI = '477c206ae68c40dda2f70e9d696193ba'
symbol = 'AAPL'
interval = '1day'

url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={stockAPI}'

response = requests.get(url)
stockInfo = response.json()
print(stockInfo)

stockName = stockInfo['meta']['symbol']
stockPrice = float(stockInfo['values'][0]['open'])
stockHigh = float(stockInfo['values'][0]['high'])
stockLow = float(stockInfo['values'][0]['low'])

print(f'Stock Name: {stockName}. Stock Current Price: ${stockPrice:.2f} Stock Low Price: ${stockLow:.2f} Stock High Price: ${stockHigh:.2f}')

