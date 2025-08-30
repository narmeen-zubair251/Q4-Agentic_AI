from agents import Agent , Runner , function_tool , RunContextWrapper , trace
from connection import config
import asyncio
import rich
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Creating Class
class CartItems(BaseModel):
    product : list
    user_id : int
    brand : str 
    total_amount : int
    discount : int

# Class Instance
cart = CartItems(
    product = ["Mobile" , "Laptop"] , 
    user_id = "00213789" , 
    brand = "apple" , 
    total_amount = 5672000 , 
    discount = 5000)

@function_tool
async def get_cartItems(wrapper : RunContextWrapper[CartItems]):
    print("Checking Context", wrapper)
    return f'{wrapper.context}'


personal_agent = Agent(
    name = "Personal Agent",
    instructions  = "You are a helpful assisstant"
)

async def main():
    result = await Runner.run(
        personal_agent ,
        'Display cart items',
        run_config = config,
        context = cart  # Making local context accessable
        )
    rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())