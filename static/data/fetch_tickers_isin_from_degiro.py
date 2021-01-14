import os
import requests
import json
import pandas as pd

'''
Here you have just to set your session id you find on your browser

'''

url = 'https://trader.degiro.nl/product_search/secure/v5/stocks?isInUSGreenList=false&stockCountryId={v0}&offset={v1}&limit={v2}&requireTotal=true&sortColumns=name&sortTypes=asc&intAccount=115000116&sessionId={v3}'
sessionId = '4932798656EE485BAA722840D34A54CC.prod_b_112_2'  # your actual session id
countryId = '846'  # 846 for American mkt
offset = [0, 1000, 2000, 3000, 4000, 5000]
limit = 1000  # limit per request

ticker_list = []
isin_list = []

for i in offset:
    request = requests.get(url.format(v0=countryId, v1=i, v2=limit, v3=sessionId))
    todos = json.loads(request.text)
    for j in todos['products']:
       ticker_list.append(j['symbol'])
       isin_list.append(j['isin'])

project_root = os.path.dirname(os.path.dirname(__file__))
data_tuples = list(zip(ticker_list,isin_list))
df = pd.DataFrame(data_tuples, columns=['tickers','isin'])
df.to_excel(r'All2.xlsx', sheet_name='all', index = False)
