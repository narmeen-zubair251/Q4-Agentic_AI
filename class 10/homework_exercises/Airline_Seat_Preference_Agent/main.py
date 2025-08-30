from agents import Agent , Runner , RunContextWrapper , trace
from connection import config
import asyncio
import rich
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
# Airline Seat Preference Agent

# Creating Class
class Airline_reserver(BaseModel):
    seat_preference : str
    travel_experience : str

airline_reserver = Airline_reserver(
    seat_preference = "Window" ,
    travel_experience = "First Time",
)

# Dynamic Instructions with conditions depend on seat prference and travel experience of the user
def my_dynamic_instructions(ctx:RunContextWrapper , agent : Agent):
    if ctx.context.seat_preference == "Window" and ctx.context.travel_experience == "First Time":
        return "Explain window benefits, mention scenic views, reassure about flight experience"
    
    elif ctx.context.seat_preference == "Middle" and ctx.context.travel_experience == "Frequent" :
        return "Acknowledge the compromise, suggest strategies, offer alternatives"
    
    elif ctx.context.seat_preference == "Any" and ctx.context.travel_experience == "Premium":
        return "Highlight luxury options, upgrades, priority boarding"

# main agent that execute in runner function
seat_reserver_agent = Agent(
    name = "Agent",
    instructions = my_dynamic_instructions,
)
 
# ------------- Runner ---------------
async def main():
    with trace("Learn Dynamic Instructions"):
        result = await Runner.run(
            seat_reserver_agent, 
            'give me some tips to make my travel comfortable and memorable',
            run_config=config,
             context = airline_reserver #Local context
            )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
