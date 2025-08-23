from agents import Agent , Runner , function_tool , RunContextWrapper
import asyncio
from pydantic import BaseModel
import rich
from connection import config

class Stu_Info(BaseModel):
    stu_id : int | str 
    student_name : str 
    current_semester : int
    total_courses : int 

student = Stu_Info(
    stu_id = "STU-456" ,
    student_name = "Hassan Ahmed" ,
    current_semester = 4 ,
    total_courses = 5
    )

@function_tool
def get_stu_info(wrapper : RunContextWrapper[Stu_Info]):
    return f'The Student Informaton is {wrapper.context}'

stu_profile = Agent(
    name = "Student" ,
    instructions = """You are a helpful assisstant. Your task is to call the tool 
    when the user asks about student profile information and when the user asks 
    about specific field so answer only about that.
    """ ,
    tools = [get_stu_info]
)

async def main():
    result = await Runner.run(
        stu_profile ,
        # 'provide me the student id and the current semester',
        'provide me the student information' ,
        run_config = config ,
        context = student
    )
    rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())