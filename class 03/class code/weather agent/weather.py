from agents import Agent , Runner , function_tool
from connection import config

@function_tool
def get_weather(City):
    return 'Today {City} weather is cloudy'

agent = Agent (
    name = "Weather Agent",
    instructions = 
"""  You are a helpful assistant . Your task to help user with weather queries.

""" ,
    tools = [get_weather]
)

result = Runner.run_sync(agent , 'What is Todays weather in Lahore , Pakistan?' ,
                         run_config = config
                        )

print(result.final_output)
