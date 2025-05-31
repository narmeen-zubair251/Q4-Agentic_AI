# ✅ installed required dependencies
# pip install openai-agents
# pip install python-dotenv

# Added api key in .env

import streamlit as st
import asyncio
from agents import Agent , AsyncOpenAI ,OpenAIChatCompletionsModel , RunConfig , Runner
from dotenv import load_dotenv
import os  #operating system

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
print(gemini_api_key)

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

translator = Agent(
    name = "Translator Agent", 
    instructions = """You are a translator. Detect the language of the input text 
    and translate it into English only. Always reply with a fluent and 
    grammatically correct English version of the text."""
)
async def translate_text(input_text):
    response = await Runner.run(
        translator,
        input=input_text,
        run_config=config
    )
    return response.final_output

st.set_page_config(page_title="Multilingual to English Translator")
st.title("🌐 Multilingual to English Translator")

st.markdown("""
## Welcome to the Smart Multilingual Translator! 👏  
A multilingual AI-powered translator that detects any language and instantly translates it into fluent English using Google's Gemini API 🤖.
""")


input_text = st.text_area("**Enter text to translate (any language):** ")

if st.button("Translate to English"):
    if input_text.strip() == "":
        st.warning("⚠ Please enter some text to translate.")
    else:
        with st.spinner("Translating...."):
          translated_text = asyncio.run(translate_text(input_text))

        st.success("Translation Completed..")
        st.write("**Translated Text:**")
        st.write(translated_text)
