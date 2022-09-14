import requests
import json
from binance.spot import Spot

#fetch the composite index symbol information
r = requests.get('https://fapi.binance.com/fapi/v1/indexInfo?symbol=FOOTBALLUSDT')
data = json.loads(r.text)

# read the api file
try:
    file = open("api_key.txt", "r")
except:
    print("找不到api_key.txt")
    input('please input any key to exit')
for line in file:
    if line.strip() == 'API Key':
        api_key = next(file, '').strip()
    elif line.strip() == 'Secret Key':
        sercret_key = next(file, '').strip()
try:
    client = Spot(key=api_key, secret=sercret_key)
    data_account = client.account()
except:
    print("API 錯誤")
    input('please input any key to exit')
file.close()
# read the account balance
for key in data_account['balances']:
    if key['asset'] == 'USDT':
       print ('帳戶餘額'+':'+key['free']+" USDT")
       balance = float(key['free'])
WantToBuy = float(input("輸入欲購買總額(USDT):"))


# Post a new order
for i in data['baseAssetList']:
    trade_pair = i['baseAsset']+'USDT'
    ask_price = float(client.book_ticker(trade_pair)['askPrice'])
    params = {
        'symbol': trade_pair,
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': round(WantToBuy*float(i['weightInPercentage'])/ask_price,1)
        
    }
    print(params)
    try:
        response = client.new_order(**params)
        print(i['baseAsset']+':'+response['status'])
    except:
        print("餘額不足或單筆訂單小於10U")

input('please input any key to exit')