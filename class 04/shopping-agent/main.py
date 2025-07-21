from agents import Agent, Runner, function_tool , AsyncOpenAI , OpenAIChatCompletionsModel, RunConfig 
from dotenv import load_dotenv
import os
from connection import config
import requests
import rich

#Loads the .env file which contains GEMINI_API_KEY
load_dotenv()

#Retrieves Gemini API key from the environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key :
    raise ValueError("Your GEMINI_API_KEY is not set .")

#Setting up the geimini Api model
external_client = AsyncOpenAI(
    api_key = gemini_api_key ,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash" ,
    openai_client = external_client ,
)

config = RunConfig(
    model = model ,
    model_provider = external_client ,
    tracing_disabled = True
)

#Creating a function as a tool which sends request to website API tp get products data
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

#Runnig the agent
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