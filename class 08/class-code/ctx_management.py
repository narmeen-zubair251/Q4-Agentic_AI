from agents import Agent , Runner , function_tool , RunContextWrapper
import asyncio
from pydantic import BaseModel
import rich 
from connection import config

#Practicing context management

class UserInfo(BaseModel):
    user_id : int | str 
    name : str
#This will be passed as context in runner
user = UserInfo(user_id = 123123 , name = "Narmeen Zubair")

@function_tool
def get_user_info(wrapper : RunContextWrapper[UserInfo]):
    return f'the user info is {wrapper.context}'

personal_agent = Agent(
    name = "Personal Agent" ,
    instructions = "You are a helpful assisstant. Your task is to call the tool to get user's information" ,
    tools = [get_user_info]
)

async def main():
    result = await Runner.run(
        personal_agent ,
        'Tell me my name and my user id' ,
        run_config = config ,
        context = user  #Local Context
        )
    rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())