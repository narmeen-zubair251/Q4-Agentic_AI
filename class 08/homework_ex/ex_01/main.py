from agents import Agent , Runner , function_tool , RunContextWrapper
import asyncio
from pydantic import BaseModel
import rich
from connection import config

class BankInfo(BaseModel):
    acc_no : str
    customer_name : str
    bank_balance : int | None = None  #Optional
    account_type : str | None = None #Optional
    

my_info = BankInfo(acc_no = "ACC-789456" , customer_name = "Narmeen Zubair" , bank_balance = 500000, account_type = "savings")

@function_tool
def get_bank_info(wrapper : RunContextWrapper[BankInfo]):
    return f'The customer informaton  is {wrapper.context}'

bank_agent = Agent(
    name = "Bank Agent" ,
    instructions = """You are a bank agent.When the user asks about customer information, 
    call the tool and request only the specific field they asked for 
    (like account number, balance, customer name, or account type) and if the user asks for whole 
    information so you can provid it.""" ,
    tools = [get_bank_info]
)

async def main():
    result = await Runner.run(
        bank_agent , 
        'give me bank_balance of the customer',
        run_config = config ,
        context = my_info
        )
    rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
