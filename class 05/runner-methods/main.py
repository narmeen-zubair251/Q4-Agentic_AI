from agents import Agent, Runner
from connection import config
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

async def main():
    agent = Agent(
        name="assistant",
        instructions="You are a helpful assistant. Help the user with its queries."
    )

    result = Runner.run_streamed(
        agent,
        "Generate 5 paragraphs about the problems of Pakistan",
        run_config=config,
    )

    async for event in result.stream_events():
    
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
