import os
from dotenv import load_dotenv
import chainlit as cl
from google.generativeai import configure, generate_text

# Load environment variables from .env file
load_dotenv()

# Configure Gemini Pro API
configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Chainlit
@cl.on_chat_start
async def start_chat():
    """Initialize the chat session."""
    cl.user_session.set("chat_history", [])

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming user messages."""
    # Retrieve chat history from the user session
    chat_history = cl.user_session.get("chat_history", [])
    
    # Append user message to chat history
    chat_history.append({"role": "user", "content": message.content})
    
    # Generate response using Gemini Pro API
    response = generate_text(
        model="gemini-1.5-pro-latest",
        prompt=f"{chat_history[-1]['content']}",
        temperature=0.7,
        max_output_tokens=150,
        top_p=0.9,
        top_k=40,
    )
    
    # Append assistant response to chat history
    chat_history.append({"role": "assistant", "content": response.text})
    
    # Update chat history in the user session
    cl.user_session.set("chat_history", chat_history)
    
    # Send the response back to the user
    await cl.Message(
        content=response.text,
        author="Assistant"
    ).send()
