import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
# 1. Imports from langchain_classic for the ReAct architecture
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from tools.search_tool import search_news

# Try to load local .env, but don't crash if it's missing (e.g., in the cloud)
load_dotenv() 

# This safely gets the key from local environment OR Streamlit Secrets
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

# Pass the key to the ChatGroq model
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0, 
    api_key=GROQ_API_KEY
)

# Define the Prompt Template
template = """
You are a professional fact-checking agent. Given a news headline:
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

Remember: Always provide Final Answer as valid JSON even if search results are limited.
"""

PROMPT = PromptTemplate.from_template(template)

# Setup Tools
tools = [search_news]

# Construct the Agent
agent = create_react_agent(llm, tools, PROMPT)

# Create the Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=15,
    max_execution_time=60,
    handle_parsing_errors=True
)

def check_news(headline: str) -> str:
    # Use .invoke() for modern compatibility
    result = agent_executor.invoke({"input": headline})
    return result["output"]