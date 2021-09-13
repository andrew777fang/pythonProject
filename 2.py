import finnhub
finnhub_client = finnhub.Client(api_key="c4m8ur2ad3icjh0eek9g")

print(finnhub_client.quote('AAPL'))
#