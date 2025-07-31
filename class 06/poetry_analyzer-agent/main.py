from agents import Agent , Runner , trace
from connection import config
from dotenv import load_dotenv
import asyncio

load_dotenv()

lyrical_agent = Agent(
    name = "lyrical_agent",
    instructions = """You are a lyrical agent. Your task is to analyze the poetry and tells that is the lyrical poetry. 
    Lyrical poetry is when the poet write about their own feelings and toughts."""
)

narrative_agent = Agent(
    name = "narrative_agent",
    instructions = """You are a narrative agent. Your task is to analyze the poetry and tells that it is a narrative poetry. 
    Narrative poetry is the poetry which tells a story with characters and events, just like a regular story but written 
    in poem form with rhymes or special rhythm"""
)

dramatic_agent = Agent(
    name = "dramatic_agent",
    instructions = """You are a dramatic agent . Your task is to analyze the poetry and tells that it is a dramatice poetry.
    Dramatic poetry is the poetry which is  meant to be performed out loud, where someone acts like a character and speaks 
    their thoughts and feelings to an audience."""
)

parent_agent = Agent(
    name = "parent_agent",
    instructions = """You are a poetry agent . Your task is to analyze the given poetry and deligate it to an 
    appropraite agent for tashree. deligate the lyrical_poetry to the lyrical agent , narrative poetry to the narrative agent and 
    dramatic poetry to the dramatic agent . if the user inputs the poetry other than all these, then keep the query to yourself 
    and gratefully deny the user query""",
    handoffs = [lyrical_agent , narrative_agent , dramatic_agent]
)

async def main():
    with trace("poetry_analyzer-agent"):
      result = await Runner.run(
         parent_agent,
         """Beneath the stars, the silence sings,
            Of whispered dreams on moonlit wings.""",
         run_config = config)
      print(result.final_output)
      print("Last Agent ==> " , result.last_agent.name)

if __name__ == "__main__":
   asyncio.run(main())

