# tools.py
from langchain.agents import Tool
from flight_search_agent import MOCK_FLIGHTS, search_flights
from policy_agent import check_policy
from purchase_agent import purchase_flight
import ast
import json
import streamlit as st

# Search Flights Tool
# Input format: "departure_city,arrival_city,date"
def _search_flights_wrapper(query: str):

    parts = query.split(",")
    if len(parts) != 3:
        return "Error: please provide departure_city, arrival_city, and date in 'CityA,CityB,YYYY-MM-DD' format."

    dep_city, arr_city, flight_date = [p.strip() for p in parts]

    matched = []
    for f in MOCK_FLIGHTS:
        if (f["departure_city"].lower() == dep_city.lower() and
            f["arrival_city"].lower() == arr_city.lower() and
            f["departure_date"] == flight_date):
            matched.append(f)
    if not matched:
        return "No flights found for that route and date."
    
    return str(matched)

    
search_flights_tool = Tool(
    name="search_flights_tool",
    func=_search_flights_wrapper,
    description=(
        "Use this tool to search flights between two cities. "
        "Input must be a string in the format 'departure_city,arrival_city'."
    )
)

#####

# Policy Check Tool
def _policy_check_wrapper(flight_data_str: str):
    
    try:
        # Safely parse string to Python object (list or single dict)
        flight_data = ast.literal_eval(flight_data_str)
    except Exception:
        return "Invalid flight data format. Please provide valid flight info."

    # If it's a list, check each flight; otherwise, it's a single flight dict
    if isinstance(flight_data, dict):
        flight_data = [flight_data]  # convert to list for uniform handling

    results = []
    for flight in flight_data:
        compliant, message = check_policy(flight)
        if compliant:
            results.append(f"Flight {flight['flight_code']} complies with policy.")
        else:
            results.append(f"Flight {flight['flight_code']} FAILS policy: {message}")

    return "\n".join(results)


policy_check_tool = Tool(
    name="policy_check_tool",
    func=_policy_check_wrapper,
    description=(
        "Check if the provided flight or flights meet corporate policy. "
        "Input is a string representing a flight dict or a list of flight dicts."
    )
)

#####

# Purchase Ticket Tool
def _purchase_flight_wrapper(json_input: str):

    try:
        flight_data = ast.literal_eval(json_input)
    except Exception:
        return "Failed to parse flight data. Please provide valid flight info (as dict/JSON)."

    if not isinstance(flight_data, dict):
        return "Purchase tool expects a single flight dict."

    return purchase_flight(flight_data)

purchase_ticket_tool = Tool(
    name="purchase_ticket_tool",
    func=_purchase_flight_wrapper,
    description=(
        "Mock process of purchasing a flight. Input must be a string that can "
        "be parsed into a dict containing flight details."
    )
)

#####

# Retrieve Past Purchases Tool
def _retrieve_past_purchases(_input: str = None):

    if "past_purchases" not in st.session_state or not st.session_state.past_purchases:
        return "No past purchases found."
    
    return json.dumps(st.session_state.past_purchases, indent=2)

retrieve_past_purchases_tool = Tool(
    name="retrieve_past_purchases_tool",
    func=_retrieve_past_purchases,
    description=(
        "Use this to get the user's past purchased flights. "
        "It returns a JSON list of purchases or a message if none found."
    )
)