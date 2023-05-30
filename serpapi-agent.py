import os
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

# Set the OpenAI API key
openai_api_key = "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"

# Set the SERP API key
serpapi_api_key = "6733c3b006db8fe32843a45cb5b0266586b48d6c81a0d2f92997d38829b8feec"

# First, let's load the language model we're going to use to control the agent.
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

# Next, let's load some tools to use. Note that the `llm-math` tool uses an LLM, so we need to pass that in.
tools = load_tools(["serpapi", "llm-math"], llm=llm, serpapi_api_key=serpapi_api_key)

# Finally, let's initialize an agent with the tools, the language model, and the type of agent we want to use.
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Now let's test it out!
agent.run("What are nice things to do in St. John, New Foundland?")
