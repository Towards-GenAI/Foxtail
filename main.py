##© 2024 Tushar Aggarwal. All rights reserved.(https://tushar-aggarwal.com)
##Foxtail [Towards-GenAI] (https://github.com/Towards-GenAI)
##################################################################################################
#Importing dependencies
from langchain import hub
from langchain.agents import Tool, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper
import os
from typing import TypedDict, Annotated, Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
import operator
from typing import TypedDict, Annotated
from langchain_core.agents import AgentFinish
from langgraph.prebuilt.tool_executor import ToolExecutor
from langgraph.prebuilt import ToolInvocation
from langgraph.graph import END, StateGraph
from langchain_core.agents import AgentActionMessageLog
import streamlit as st
from dotenv import load_dotenv
##################################################################################################
load_dotenv()
st.set_page_config(page_title="Foxtail Agent", layout="wide")























os.getenv("GOOGLE_API_KEY") 
os.getenv["SERPER_API_KEY"]


search = GoogleSerperAPIWrapper()

#Tools
def toggle_case(word):
            toggled_word = ""
            for char in word:
                if char.islower():
                    toggled_word += char.upper()
                elif char.isupper():
                    toggled_word += char.lower()
                else:
                    toggled_word += char
            return toggled_word

def sort_string(string):
     return ''.join(sorted(string))
 
 
#Agents
tools = [
      Tool(
          name = "Search",
          func=search.run,
          description="useful for when you need to answer questions about current events",
      ),
      Tool(
          name = "Toogle_Case",
          func = lambda word: toggle_case(word),
          description = "use when you want covert the letter to uppercase or lowercase",
      ),
      Tool(
          name = "Sort String",
          func = lambda string: sort_string(string),
          description = "use when you want sort a string alphabetically",
      ),

        ]



















def main():
    # Streamlit UI elements
    st.title("LangGraph Agent + Gemini Pro + Custom Tool + Streamlit")

    # Input from user
    input_text = st.text_area("Enter your text:")
    
    if st.button("Run Agent"):
        
        












































































