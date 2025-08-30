from agents import Agent , Runner , RunContextWrapper , trace
from connection import config
import asyncio
import rich
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Medical Consultant Agent

class Assistant(BaseModel):
    name : str
    user_type : str

medical_assistant = Assistant(
    name = "Narmeen" ,
    user_type = "doctor" ,
)

# Dynamic Instructions with conditions based on user type
def my_dynamic_instructions(ctx : RunContextWrapper , agent : Agent):
    if ctx.context.user_type == "patient" :
        return "Use simple, non-technical language. Explain medical terms in everyday words. Be empathetic and reassuring."
    
    elif ctx.context.user_type == "medical-student":
        return "Use moderate medical terminology with explanations. Include learning opportunities."
    
    elif ctx.context.user_type == "doctor":
        return "Use moderate medical terminology with explanations. Include learning opportunities."
    
# main agent
medical_agent = Agent(
    name = "Medical Agent",
    instructions = my_dynamic_instructions

)

# ----------- Runner -----------
async def main():
    result = await Runner.run(
        medical_agent ,
        'suuggest me precautions about Blood Pressure',
        run_config = config ,
        context = medical_assistant
    )
    rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())