# tools.py
from langchain.agents import Tool
from flight_search_agent import search_flights
from policy_agent import check_policy
from purchase_agent import purchase_flight
import ast

def _flight_search_wrapper(city_pair: str):
    try:
        departure, arrival = city_pair.split(",")
    except ValueError:
        return "Please provide two cities, separated by a comma."
    
    results = search_flights(departure.strip(), arrival.strip())
    if results:
        return str(results)  # Return them as a string so LLM can read them
    else:
        return "No flights found."
    
    
search_flights_tool = Tool(
    name="search_flights_tool",
    func=_flight_search_wrapper,
    description=(
        "Use this tool to search flights between two cities. "
        "Input must be a string in the format 'departure_city,arrival_city'."
    )
)

#####

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

def _purchase_flight_wrapper(json_input: str):
    """
    The LLM will call this tool with a string that can be parsed as a Python dict.

    Expected input format (as a string):
    {
      "flight_code": "TK103",
      "carrier": "THY",
      "departure_city": "Istanbul",
      "arrival_city": "Ankara",
      "class": "Economy",
      "price": 1950
    }
    """
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