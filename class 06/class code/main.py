from agents import Agent , Runner , function_tool , trace
from connection import config
import asyncio
from dotenv import load_dotenv


load_dotenv()

@function_tool
def weather():
    return "Rainy"

@function_tool
def current_location():
    return "Karachi"

plant_agent = Agent(
    name = "plant_agent",
    instructions = "You are a plant agent . Your task is to answer user queries related to plants."
)

medicine_agent  = Agent(
    name = "medicine_agent",
    instructions = "You are a medicine agent .Your task is to answer user query related to medicines.",
    model = "gpt3"
)

parent_agent = Agent(
    name = "parent_agent",
    instructions = """You are a parent agent. Your task is to deligate user queries to an appropriate agent.
    Queries related to plants and flowers will e deligated to plant agent and the queries related to medicines 
    and body systems will deligated to medicine agent.
    Queries other than these will be kept to your self and gratefully deny to the user """,
    handoffs = [medicine_agent , plant_agent],
    tools = [weather , current_location]
)

async def main():
    with trace("class code"):
     result = await Runner.run(
        parent_agent ,
        "What is photosynthesis? and what is my current location? and tell me about wheather also." ,
        run_config = config
    )
     print(result.final_output)
     print("Last agent ==> " ,result.last_agent.name)

if __name__ == "__main__" :
    asyncio.run(main())   
