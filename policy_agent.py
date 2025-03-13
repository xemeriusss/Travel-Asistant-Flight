def check_policy(flight):
    if flight["price"] > 2000:
        return (False, f"Flight {flight['flight_code']} is over the 2000 TL limit.")
    if flight["class"].lower() != "economy":
        return (False, f"Flight {flight['flight_code']} is not Economy class.")
    return (True, "OK")
