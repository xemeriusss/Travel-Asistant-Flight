def purchase_flight(flight_dict):
    """
    Mock purchase. In a real scenario, you'd call an external API here.
    Return a success or failure message.

    flight_dict: a Python dict with flight details (flight_code, carrier, etc.).
    """
    flight_code = flight_dict.get("flight_code", "Unknown")
    carrier = flight_dict.get("carrier", "Unknown")

    return (
        f"Purchase successful!\n"
        # f"Flight: {flight_code} ({carrier})\n"
        "Thank you for booking with us!"
    )
