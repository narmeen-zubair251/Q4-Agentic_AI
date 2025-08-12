from agents import Agent , Runner , input_guardrail , GuardrailFunctionOutput , InputGuardrailTripwireTriggered , output_guardrail , OutputGuardrailTripwireTriggered
from dotenv import load_dotenv
from connection import config
import asyncio
from pydantic import BaseModel
import rich

class PassengerOutput(BaseModel):
    response : str 
    isWeightExceed : bool

airprt_security_guard = Agent(
    name = "airport_security_guard",
    instructions = """ Your task is to check the passenger's laggage. If Passenger's 
    laggage is more than 25Kgs , gracefully stop them.
""" , 
    output_type = PassengerOutput
)

@input_guardrail
async def Security_guardrail(ctx , agent , input):
    result = await Runner.run(airprt_security_guard ,
                               input , # same input in main runner function
                               run_config = config)
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info = result.final_output.response ,
        tripwire_triggered = result.final_output.isWeightExceed  # Creating it dynamic 
    )
# Main Agent
Passenger_agent = Agent(
    name = "Passenger_agent",
    instructions = "You are a Passenger Agent",
    input_guardrails = [Security_guardrail]
)

async def main():
    try:
      result = await Runner.run(Passenger_agent , "My laggage is 20Kgs" , run_config = config)
      print("Passenger is onboarded")
    except InputGuardrailTripwireTriggered:
        print("Passenger can not check-in")


# -------OUTPUT GUARDRAIL--------
class MessageOutput(BaseModel):
    response : str

class PHDOutput(BaseModel):
    isPHDLevelResponse : bool

phd_guardrail_agent = Agent(
    name = "Phd Guardrail Agent",
    instructions = """
        You are a PHD Guardrail Agent that evaluates if text is too complex for 8th grade students. If the response if 
        very hard to read for an eight grade student deny the agent response.
""" ,
    output_type = PHDOutput
)

@output_guardrail
async def PHd_guardrail(ctx , agent:Agent , output) -> GuardrailFunctionOutput:
    result = await Runner.run(phd_guardrail_agent , output.response , run_config = config)
    
    return GuardrailFunctionOutput(
        output_info = result.final_output ,
        tripwire_triggered = result.final_output.isPHDLevelResponse
    )

#  Main executor agent
eight_grade_agent = Agent(
    name = "Eight Grade Student",
    instructions = """
        1. You are an agent that answer query to a eight standard student. Keep your vocabulary simple and easy. 
        2. If asked to give answers in most difficult level use the most hardest english terms
""" ,
    output_type = MessageOutput ,
    output_guardrails = [PHd_guardrail]
)


async def og_main():
    query = "What are trees? Explain using the most complex scientific terminology possible" , 
    try:
        result = await Runner.run(eight_grade_agent , query , run_config = config)
        print(result.final_output)
    except  OutputGuardrailTripwireTriggered:
        print("Agent Output is not according to expectations.")

if __name__ == "__main__":
    asyncio.run(og_main())
    asyncio.run(main())