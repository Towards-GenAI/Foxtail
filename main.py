##© 2024 Tushar Aggarwal. All rights reserved.(https://tushar-aggarwal.com)
##Foxtail [Towards-GenAI] (https://github.com/Towards-GenAI)
##################################################################################################
# Importing dependencies
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
import google.generativeai as genai
##################################################################################################
load_dotenv()
st.set_page_config(page_title="Foxtail Agent", layout="wide")

google_api_key = os.getenv("GOOGLE_API_KEY")
search = GoogleSerperAPIWrapper()

# Tools
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

# Agents 
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events",
    ),
    Tool(
        name="Toggle_Case",
        func=lambda word: toggle_case(word),
        description="use when you want to convert the letters to uppercase or lowercase",
    ),
    Tool(
        name="Sort_String",
        func=lambda string: sort_string(string),
        description="use when you want to sort a string alphabetically",
    ),
]

prompt = hub.pull("hwchase17/react")

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=google_api_key,
    convert_system_message_to_human=True,
    verbose=True,
)

agent_runnable = create_react_agent(llm, tools, prompt)

class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    return_direct: bool
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]

tool_executor = ToolExecutor(tools)

def run_agent(state):
    agent_outcome = agent_runnable.invoke(state)
    return {"agent_outcome": agent_outcome}

def execute_tools(state):
    messages = [state['agent_outcome']]
    last_message = messages[-1]
    tool_name = last_message.tool
    arguments = last_message
    if tool_name in ["Search", "Sort_String", "Toggle_Case"]:
        if "return_direct" in arguments:
            del arguments["return_direct"]
    action = ToolInvocation(
        tool=tool_name,
        tool_input=last_message.tool_input,
    )
    response = tool_executor.invoke(action)
    return {"intermediate_steps": [(state['agent_outcome'], response)]}

def should_continue(state):
    messages = [state['agent_outcome']]
    last_message = messages[-1]
    if "Action" not in last_message.log:
        return "end"
    else:
        arguments = state["return_direct"]
        if arguments is True:
            return "final"
        else:
            return "continue"

def first_agent(inputs):
    action = AgentActionMessageLog(
        tool="Search",
        tool_input=inputs["input"],
        log="",
        message_log=[]
    )
    return {"agent_outcome": action}

workflow = StateGraph(AgentState)

workflow.add_node("agent", run_agent)
workflow.add_node("action", execute_tools)
workflow.add_node("final", execute_tools)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "final": "final",
        "end": END
    }
)

workflow.add_edge('action', 'agent')
workflow.add_edge('final', END)

app = workflow.compile()

def main():
    # Streamlit UI elements
    st.title("LangGraph Agent + Gemini Pro + Custom Tool + Streamlit")

    # Input from user
    input_text = st.text_area("Enter your text:")
    
    if st.button("Run Agent"):
        inputs = {"input": input_text, "chat_history": [], "return_direct": False}
        results = []
        for s in app.stream(inputs):
            result = list(s.values())[0]
            results.append(result)
            st.write(result)  # Display each step's output
            
if __name__ == "__main__":
    main()