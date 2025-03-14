import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from tools import search_flights_tool, policy_check_tool, purchase_ticket_tool

load_dotenv()

def create_agent():
    # 1. List of tools the agent has access to:
    tools = [search_flights_tool, policy_check_tool, purchase_ticket_tool]

    # 2. Agent uses an LLM to process the user query and generate a response
    llm = ChatGoogleGenerativeAI(
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.0-flash",
        temperature=0.7
    )

#     # 3. The agent's prompt
#     prefix = """You are a travel assistant. You can answer queries about flights.
# When it's relevant, use the provided tools to find flight data.
# If user asks something out of scope, respond with "I'm sorry, I only handle flight queries." 
# -----
# """
#     suffix = """Begin:
# {chat_history}
# Question: {input}
# {agent_scratchpad}"""


    # A prefix instructing the agent how to respond
    prefix = """You are a travel assistant that strictly follows corporate policy:
1) Any flight above 2000 TL is not allowed.
2) Only Economy class is allowed.

You have the following tools:
1) search_flights_tool - to find flights between two cities, format: "CityA,CityB"
2) policy_check_tool - to verify flights' compliance with the above policy
3) purchase_ticket_tool: finalize the purchase of a flight.

When the user asks for flights, do:
- Use search_flights_tool to get the flights.
- Then use policy_check_tool for each flight or for the entire list.
- Recommend only flights that comply with policy.

When the user wants to purchase a flight:
- Make sure the flight is policy-compliant.
- Then use 'purchase_ticket_tool' to mock a ticket purchase.

Give a proper answer as sentences, not in json format.
If the user asks something outside flight scope, respond: "I'm sorry, I only handle flight queries."

-----
"""
    # The suffix includes placeholders for the conversation
    suffix = """Begin:
{chat_history}
Question: {input}
{agent_scratchpad}"""


    # Create the prompt
    prompt = ZeroShotAgent.create_prompt(
        tools=tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "chat_history", "agent_scratchpad"]
    )

    # Create an LLMChain first
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt
    )

    # 4. Create the ZeroShotAgent with the LLM chain
    agent = ZeroShotAgent(
        llm_chain=llm_chain,
        tools=tools,
        verbose=True
    )

    # 5. Create an AgentExecutor that handles the full logic
    agent_chain = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_chain


