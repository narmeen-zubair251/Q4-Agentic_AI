from agents import Agent, Runner, function_tool  
from connection import config
import requests



@function_tool
def get_crypto_price(coin: str = "bitcoin", currency: str = "usd") -> str:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}"
    response = requests.get(url)
    data = response.json() 

    if coin in data and currency in data[coin]: 
        price = data[coin][currency] # Agar coin + currency dono mil jayein: Price return karo readable format mein.
        return f"The current price of {coin.capitalize()} is {price} {currency.upper()}."
    else:
        return "Cryptocurrency not found or API error."



# Create Agent
agent = Agent(
    name="Crypto Agent",
    instructions="""As a Crypto Agent, your job is to track 
    the pulse of the crypto market in real-time and respond instantly. 
    If the user does not mention a currency, assume 'usd' by default. 
    Use the get_crypto_price tool to fetch prices of cryptocurrencies.""",
    tools=[get_crypto_price]
)

# Run the Agent
result = Runner.run_sync(
    agent, 
    input="Tell me the price of bitcoin and ethereum today?", 
    run_config=config
)

print(result.final_output)
