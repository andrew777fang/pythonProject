import finnhub
finnhub_client = finnhub.Client(api_key="c4m8ur2ad3icjh0eek9g")
print(finnhub_client)
res=finnhub_client.stock_candles("SLV","D",1590988249,1591852249)
print(res)