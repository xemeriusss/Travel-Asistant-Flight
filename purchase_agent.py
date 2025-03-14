def purchase_flight(flight_dict):
    """
    Mock the purchase process. In a real scenario, you'd call an external payment API.
    Returns a success message or an error message.
    """
    # Here, we assume 'flight_dict' is a Python dict with keys like flight_code, carrier, etc.
    flight_code = flight_dict.get("flight_code", "Unknown")
    return f"Purchase successful! Your ticket for flight {flight_code} is confirmed."


