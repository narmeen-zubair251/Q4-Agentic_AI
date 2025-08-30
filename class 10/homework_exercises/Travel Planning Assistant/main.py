from agents import Agent , Runner , RunContextWrapper , trace
from connection import config
import asyncio
import rich
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Travel Planning Assistant

#Creating Class
class Traveler(BaseModel):
    trip_type : str
    traveler_profile : str

TravelerOne = Traveler(
    trip_type = "Adventure" ,
    traveler_profile = "Solo" ,
)

# Dynamic Instructions that depends on trip type and traveler profile
def my_dynamic_instructions(ctx:RunContextWrapper[Traveler] , agent:Agent):
    if ctx.context.trip_type == 'Adventure' or ctx.context.traveler_profile == "Solo":
        return "Suggest exciting activities, focus on safety tips, recommend social hostels and group tours for meeting people"
    
    elif ctx.context.trip_type == 'Cultural' or ctx.context.traveler_profile == "Family":
        return "Focus on educational attractions, kid-friendly museums, interactive experiences, family accommodations."
    
    elif ctx.context.trip_type == 'Buisness' or ctx.context.traveler_profile == "Executive":
        return "Emphasize efficiency, airport proximity, business centers, reliable wifi, premium lounges."

# main agent
personal_agent = Agent(
    name = "Agent",
    instructions = my_dynamic_instructions,
)

# ---------- Runner ----------
async def main():
    with trace("Learn Dynamic Instructions"):
        result = await Runner.run(
            personal_agent, 
            'suggest me some traveling tips',
            run_config=config,
             context = TravelerOne # Local context
            )
        rich.print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
