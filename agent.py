import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from tools import search_flights_tool, policy_check_tool, purchase_ticket_tool, retrieve_past_purchases_tool, recommend_destination_tool

load_dotenv()

def create_agent():
    # List of tools the agent has access.
    tools = [search_flights_tool, policy_check_tool, purchase_ticket_tool, retrieve_past_purchases_tool, recommend_destination_tool]

    # Agent uses an LLM to process the user query and generate a response
    llm = ChatGoogleGenerativeAI(
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-2.0-flash",
        temperature=0.7 # To control the randomness of the response
    )

    prefix = """You are a travel assistant that strictly follows corporate policy:
1) Any flight above 2000 TL is not allowed.
2) Only Economy class is allowed.

You have the following tools:
1) search_flights_tool - to find flights given (city pair, date). Format: "CityA,CityB,YYYY-MM-DD"
2) policy_check_tool - to verify flights' compliance with the above policy
2) purchase_ticket_tool - finalize the purchase of a flight.
3) retrieve_past_purchases_tool - to retrieve past purchases.
4) recommend_destination_tool - to recommend destinations based on weather.

Workflow you must follow:
1) If the user says "I want to buy a ticket" (or similar) but does not provide:
   - city pair,
   - trip type (one-way vs. round-trip),
   - travel date(s),
   ask them for each missing piece of info. 
   (For round-trip, you must also ask for the return date.)
2) When you have city pair + date(s) + trip type:
   - If trip type is "one-way", call 'search_flights_tool' with "CityA,CityB,DepartureDate".
   - If trip type is "round-trip", 
     - first call 'search_flights_tool' for the outbound segment (CityA,CityB,DepDate),
     - then call 'search_flights_tool' for the inbound segment (CityB,CityA,ReturnDate).
   Present the flights in your reply (do not purchase yet).
3) Wait for the user to pick which flight(s) they want in a subsequent message.
4) When the user says "I choose flight X" or "I want to purchase flight X," THEN call 'purchase_ticket_tool'.
   For round-trip, user may need to pick two flights (outbound and inbound).

If user tries to purchase immediately in the same message they first request flights, 
still do the search step first. The user must confirm specific flights in their next message before purchase.

If user says "show me the past purchases" or something similar, 
call 'retrieve_past_purchases_tool' to retrieve that info. Then present it in your reply in a human-friendly format.

If the user asks similar to "I want to fly somewhere hot" or "I want to fly somewhere cold", 
then call 'recommend_destination_tool' with the appropriate preference ("hot" or "cold"). 
Use its output to recommend destination cities, then ask the user if they would like to see flights to one of those destinations.

If user asks something out of scope, respond: "I'm sorry, I only handle flight queries."
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

    # Create the ZeroShotAgent with the LLM chain
    agent = ZeroShotAgent(
        llm_chain=llm_chain,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

    # Create an AgentExecutor that handles the full logic
    agent_chain = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_chain


