from agents import Agent , Runner , input_guardrail , GuardrailFunctionOutput
from connection import config
from pydantic import BaseModel
import asyncio
import rich

class AgentOutput(BaseModel):
    response : str 
    isTimeChange : bool

teacher_agent = Agent(
    name = "teacher_agent",
    instructions = """
    You are a teacher agent. Check if the student is asking to change 
    their class timing. Reply politely and set isTimeChange to True if they request a 
    change, otherwise set it to False."
""",
    output_type = AgentOutput 
)

@input_guardrail
async def Process_time_change(ctx , agent , input):
    result = await Runner.run(teacher_agent , 
                              input , 
                              run_config = config)
    rich.print(result.final_output)
    return GuardrailFunctionOutput(
        output_info = result.final_output.response ,
        tripwire_triggered = result.final_output.isTimeChange 
    )


# Main Agent 
student_agent = Agent(
    name = "Student" ,
    instructions = "You are a student agent" , 
    input_guardrails = [Process_time_change]
)

async def main():
    try:
       result = await Runner.run(student_agent , 
                              "I want to change my class timings 😭😭",
                              run_config = config)
       print("You can contact the administration team.")
    except:
       print("Sorry! You have to complete this quarter in your assigned timings.")
       

if __name__ == "__main__":
    asyncio.run(main())
