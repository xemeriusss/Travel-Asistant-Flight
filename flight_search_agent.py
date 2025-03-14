MOCK_FLIGHTS = [
    {
        "flight_code": "TK103",
        "carrier": "THY",
        "departure_city": "Istanbul",
        "arrival_city": "Ankara",
        "class": "Economy",
        "price": 1950
    },
    {
        "flight_code": "TK104",
        "carrier": "THY",
        "departure_city": "Istanbul",
        "arrival_city": "Ankara",
        "class": "Business",
        "price": 4150
    },
        {
        "flight_code": "TK105",
        "carrier": "THY",
        "departure_city": "Istanbul",
        "arrival_city": "Ankara",
        "class": "Economy",
        "price": 800
    },
    {
        "flight_code": "LH201",
        "carrier": "Lufthansa",
        "departure_city": "Berlin",
        "arrival_city": "Frankfurt",
        "class": "Economy",
        "price": 2490
    },
    {
        "flight_code": "LH202",
        "carrier": "Lufthansa",
        "departure_city": "Berlin",
        "arrival_city": "Frankfurt",
        "class": "Business",
        "price": 4990
    },
    {
        "flight_code": "BA303",
        "carrier": "British Airways",
        "departure_city": "London",
        "arrival_city": "New York",
        "class": "Economy",
        "price": 1700
    },
    {
        "flight_code": "BA304",
        "carrier": "British Airways",
        "departure_city": "London",
        "arrival_city": "New York",
        "class": "Business",
        "price": 1200
    },
    {
        "flight_code": "UA501",
        "carrier": "United Airlines",
        "departure_city": "Chicago",
        "arrival_city": "Los Angeles",
        "class": "Economy",
        "price": 3100
    },
    {
        "flight_code": "UA502",
        "carrier": "United Airlines",
        "departure_city": "Chicago",
        "arrival_city": "Los Angeles",
        "class": "Business",
        "price": 7500
    },
    {
        "flight_code": "QR701",
        "carrier": "Qatar Airways",
        "departure_city": "Doha",
        "arrival_city": "Istanbul",
        "class": "Economy",
        "price": 2800
    },
    {
        "flight_code": "QR702",
        "carrier": "Qatar Airways",
        "departure_city": "Doha",
        "arrival_city": "Istanbul",
        "class": "Business",
        "price": 1400
    }
]

def search_flights(departure_city, arrival_city):
    results = []
    for flight in MOCK_FLIGHTS:
        if (flight["departure_city"].lower() == departure_city.lower() and
            flight["arrival_city"].lower() == arrival_city.lower()):
            results.append(flight)
    return results
