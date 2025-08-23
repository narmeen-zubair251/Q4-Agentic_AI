from agents import Agent , Runner , function_tool
from connection import config

@function_tool
def usd_to_pkr():
    return 'Today USD to PKR is Rs.280'

agent = Agent (
    name = "Currency Rate",
    instructions = 
"""  You are a helpful assistant . Your task to help user with its queries.

""" ,
    tools = [usd_to_pkr]
)

result = Runner.run_sync(agent , 'What is the conversion rate of USD to PKR today?' ,
                         run_config = config
                        )

print(result.final_output)
