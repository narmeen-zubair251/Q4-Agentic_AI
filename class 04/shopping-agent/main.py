from agents import Agent, Runner, function_tool 
from connection import config
import requests
import rich

#Creating a function as a tool which sends request to website API t0 get products data
@function_tool
def get_products():
    url = "https://template-03-api.vercel.app/api/products"
    response = requests.get(url)
    return response.json()


#Creating Agent
agent = Agent(
    name = "Shopping Agent",
    instructions = """You are a smart shopping assistant 
    that helps users find, compare, and purchase products based on their preferences""",
    tools = [get_products]
)

#Running the agent
result = Runner.run_sync(
    agent , 
    input = "Show me all the product list " ,
    run_config= config
)

#Multiple queries to test the agent
test_query = [
    "Show me all available products.",
    "Can you suggest me the best shoes to buy?",
    "What products can I buy right now?",
    "Suggest me the most best products you have.",
    "Can you display all items you have?"
   
]

#Looping through each query
for query in test_query:
    rich.print(f"\n[bold cyan]User Prompt:[/bold cyan] {query}")


    result = Runner.run_sync(
    agent , 
    input = query ,
    run_config= config
)
    rich.print(f"\n[bold yellow]Agent Response:[/bold yellow] ")
    rich.print(result.final_output)
