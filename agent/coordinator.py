import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from tools.search_tool import search_news

# Load .env locally, ignore in cloud
load_dotenv() 

# Get Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0, 
    api_key=GROQ_API_KEY
)

# Setup Tools
tools = [search_news]

# Define the Prompt (Keep your template as it is)
template = """You are a professional fact-checking agent. Given a news headline:

1. Extract factual claims.

2. Search for evidence.

3. Return a JSON response with these exact keys:

   - claims: list of factual claims found

   - evidence: summary of what you found online

   - credibility_score: number from 0 to 100

   - verdict: choose EXACTLY one of these four options:

       * TRUE — if strong evidence supports the claim

       * FALSE — if evidence clearly contradicts the claim

       * MISLEADING — if claim has some truth but is exaggerated or missing context

       * UNVERIFIED — if no clear evidence found online

   - reasoning: short explanation of your verdict



IMPORTANT: Use MISLEADING when a claim is partially true but exaggerated.

Use UNVERIFIED when search results are unclear or unrelated.

Do NOT always default to TRUE or FALSE only.



You have access to these tools:

{tools}



Use this format:

Thought: think about what to do

Action: the action to take, should be one of [{tool_names}]

Action Input: the input to the action

Observation: the result of the action

... (repeat Thought/Action/Action Input/Observation as needed)

Thought: I now have enough info

Final Answer: the final JSON response



Input: {input}



{agent_scratchpad}



Remember: Always provide Final Answer as valid JSON even if search results are limited."""
PROMPT = PromptTemplate.from_template(template)

# Construct the Agent using langgraph
# Note: create_react_agent in langgraph directly returns an executor-like agent
agent_executor = create_react_agent(llm, tools, state_modifier=template)

def check_news(headline: str) -> str:
    result = agent_executor.invoke({"messages": [("user", headline)]})
    return result["messages"][-1].content