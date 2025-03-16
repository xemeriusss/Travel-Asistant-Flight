def purchase_flight(flight_dict):

    flight_code = flight_dict.get("flight_code", "Unknown")
    carrier = flight_dict.get("carrier", "Unknown")

    return (
        f"Purchase successful!\n"
        # f"Flight: {flight_code} ({carrier})\n"
        "Thank you for booking with us!"
    )
