from agents import Agent , Runner , function_tool
from connection import config
from datetime import datetime

@function_tool
def get_weather(city:str) -> str:
    return f'the weather of {city} is rainy'

@function_tool
def get_date():
    now = datetime.now()
    return now.strftime("the date is %d-%m-%Y")

#Practice Scenarios
@function_tool
def get_time():
    time_now = datetime.now()
    return time_now.strftime("The time is 10:51 PM")

@function_tool
def get_day():
    today = datetime.now()
    return today.strftime("Today is Friday")

@function_tool
def greet_user(name:str) -> str:
    return f'Hello {name}! Hope you are doing well.' 

@function_tool
def divide_numbers(a:int , b:int) -> int:
    return a % b

@function_tool
def get_capital(country: str)->str:
    capitals = {
        "Pakistan": "Islamabad",
        "India": "New Delhi",
        "Usa": "Washington",
        "Uk": "London"}
    
    capital = capitals.get(country.strip().title())

    if capital:
        return f"The capital of {country.title()} is {capital}"
    else:
        return f"Sorry i cannot provide the capital of {country.title}!"
    
@function_tool
def calculate_age(year_of_birth: int) -> str:
    current_year = datetime.now().year
    age = current_year - year_of_birth

    if age < 0 :
        return"You entered the future Year , PLease check you input!"
    return f"you are {age} years old!"

@function_tool
def get_weather(city:str)->str :
    weathers = {
        "Karachi": "Rainy" ,
        "Islamabad" : "Cloudy" ,
        "Lahore" : "Sunny" ,
        "Muree" : "Snowfall"
    }

    city = weathers.get(city.strip().title())
    
    if city:
        return f"The weather of {city.title()} is {city}"
    return "Sorry i can not provide the weather of this city!"


agent = Agent(
    name = "assistant", 
    instructions = "You are a helpful assistant",
    tools = [get_date , get_weather , get_time , get_day , greet_user , divide_numbers, get_capital, calculate_age]
)

result = Runner.run_sync(agent ,"""Tell me the weather of karachi and islamabad?""", 
                            run_config = config)
print(result.final_output)