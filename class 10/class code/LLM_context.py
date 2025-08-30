from agents import Agent , Runner , RunContextWrapper , trace
from connection import config
import asyncio
import rich
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Person(BaseModel):
    name : str
    user_level : str

PersonOne = Person(
    name = "Narmeen" ,
    user_level = "PHD" ,
)

def my_dynamic_instructions(ctx:RunContextWrapper[Person] , agent:Agent):
    if ctx.context.user_level == 'junior' or ctx.context.user_level == "MidLevel":
        return "Keep your answers simple and easy to understand"
    elif ctx.context.user_level == "PHD":
        return "Keep your vocabulary advanced like you are talking to a PHD level person"

personal_agent = Agent(
    name = "Agent",
    instructions = my_dynamic_instructions,
)

async def main():
    with trace("Learn Dynamic Instructions"):
        result = await Runner.run(
            personal_agent, 
            'What is light?',
            run_config=config,
             context = PersonOne #Local context
            )
        rich.print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())