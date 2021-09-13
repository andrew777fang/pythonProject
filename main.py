import requests
r1= requests.get\
     ('https://finnhub.io/api/v1/quote?symbol=AAPL&token=c4m8ur2ad3icjh0eek9g')
res1=r1.json()
print(res1)
# #