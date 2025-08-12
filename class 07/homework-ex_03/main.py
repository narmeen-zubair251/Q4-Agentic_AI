
from agents import Agent , Runner , input_guardrail , GuardrailFunctionOutput ,InputGuardrailTripwireTriggered
from connection import config
from pydantic import BaseModel
import rich
import asyncio

class AgentOutput(BaseModel):
    response : str 
    isOtherStudent : bool


gate_keeper = Agent(
    name = "Gate keeper" ,
    instructions = """You are a gate keeper agent. Your task is to check students 
    identity and allow enter the students of your school and stop entering the stdents 
    of other school.""" ,
    output_type = AgentOutput
)
@input_guardrail
async def gatekeeper_guardrail(ctx , agent , input):
    result = await Runner.run(gate_keeper ,
                              input ,
                              run_config = config)
    rich.print(result.final_output)
    
    return GuardrailFunctionOutput(
        output_info = result.final_output.response ,
        tripwire_triggered = result.final_output.isOtherStudent
    )

other_students = Agent(
    name = "other_students" , 
    instructions = "You are a student assistant." ,
    input_guardrails = [gatekeeper_guardrail]
)

async def main():
    try:
       result = await Runner.run(other_students , 
                              "We are the seniors came here for the visit.",
                               run_config = config)
       print("You can enter the school.😊")

    except InputGuardrailTripwireTriggered:
       print("⚠ Sorry! You are not allowed here.")

if __name__ == "__main__":
    asyncio.run(main())
