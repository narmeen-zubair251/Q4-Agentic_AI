from agents import Agent , Runner , function_tool , RunContextWrapper
import asyncio
from pydantic import BaseModel
import rich
from connection import config

class Library_info(BaseModel):
    book_id : str 
    book_title : str
    author_name : str
    is_available : bool

library_book = Library_info(
    book_id = "BOOK-123" ,
    book_title = "Python Programming" ,
    author_name = "John Smith",
    is_available = True
)

@function_tool
def get_library_info(wrapper : RunContextWrapper[Library_info]):
    return f'The library information is {wrapper.context}'


library_agent = Agent(
    name = "Library Agent",
    instructions ="""You are a helpful assistant. When the user asks about the library information 
                 or any specific field, you should call the tool and provide the requested details
                 andIf the user asks about the availability of a book also, then check the is_available field.
                 If is_available = True, respond with "Yes, available".
                 If is_available = False, respond with "No, not available.
                 and if the user asks about whole information then you will provide all details.""",
    tools = [get_library_info]
)

async def main():
    result = await Runner.run(
        library_agent ,
        # "Provide me the library book details" ,
        'give me the book_title and author name and tell me also if the book is available',
        run_config = config ,
        context = library_book
        )
    rich.print(result.final_output)
    
if __name__  == "__main__":
    asyncio.run(main())