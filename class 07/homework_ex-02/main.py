from agents import Agent , Runner , input_guardrail , GuardrailFunctionOutput
from connection import config
from pydantic import BaseModel
import rich
import asyncio

class AgentOutput(BaseModel):
    response : str 
    isSpeedExceed : bool


father_agent = Agent(
    name = "father_agent",
    instructions = """You are a father agent. Your task is to check the Ac speed , if it 
     is below 26C , then stop the child from doing that.
     """ ,
     output_type = AgentOutput
)
@input_guardrail
async def father_guardrail(ctx , agent , input):
    result = await Runner.run(father_agent , 
                              input , 
                              run_config = config)
    rich.print(result.final_output)

    return GuardrailFunctionOutput (
        output_info = result.final_output.response ,
        tripwire_triggered = result.final_output.isSpeedExceed 
    )
    

child_agent = Agent(
    name = "child_agent",
    instructions = "You are a child agent.",
    input_guardrails = [father_guardrail]
    )

async def main():
    try:
        result = await Runner.run(child_agent ,
                                 "Your Ac speed is 16C.",
                                  run_config = config
                                  )
        print("Situation is UnderControl😎")
    except:
        print("Abbu se daant paregi apko betaa😄")

if __name__ == "__main__" :
    asyncio.run(main())
