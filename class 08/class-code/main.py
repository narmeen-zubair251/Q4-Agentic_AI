from agents import Agent, GuardrailFunctionOutput, GuardrailFUnctionOutput, InputGuardrailTripwireTriggered, Runner,input_guardrail,output_guardrail , trace
from connection import config
from pydantic import BaseModel
import asyncio
from dotenv import load_dotenv
import rich

load_dotenv()

####### Understanding the First Agent logic in Input Guardrail #######

class MedicineOutput(BaseModel):
    response : str 
    isMedicinequery : bool

guardrail_agent = Agent(
    name = "guardrail agent",
    instructions = """You are a guardrail agent . Your task is to keep an eye on the 
                   user query.The user query only should be only related to medicine if 
                   the user try to give any input realted to ither things you will stop it.""",
    output_type = MedicineOutput
)

@input_guardrail
async def medicine_guardrail(ctx , agent , input) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent , input , run_config = config)
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info = result.final_output ,
        tripwire_triggered = not result.final_output
    )

medicine_agent = Agent(
    name = "medicine_agent" ,
    instructions = """You are a medicine agent . Your task is to answer user queries related to body systems and mecidine .
                    if the user asks about the best medicines for any disease , 
                   so you will give the name of the best medicines for their need first 
                   then give a disclaimer to consult the doctor once before taking action 
                   on my recommendation."""
)

triage_agent = Agent(
    name = "Triage_agent" ,
    instructions = "You are a triage agent.Your task is to delegate the task to an appropriate agent." ,
    handoffs = [medicine_agent] ,
    input_guardrails = [medicine_guardrail]

)

async def main():
    with trace("Learning Guardrails"):
      try:
        result = await Runner.run(triage_agent ,
                                  "What is the most recommended medicine for blodd pressure?" , 
                                   run_config = config)
        print(result.final_output)
      except InputGuardrailTripwireTriggered:
        print("Agent Output is not according to the expectations.")

if __name__ == "__main__":
    asyncio.run(main())


