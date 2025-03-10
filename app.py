import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Amadeus API Credentials
API_KEY = "NUr5GWYPyRkuieBC8locpeNUWzLL65hB"
API_SECRET = "BQyVvOw4vbsXbfxh"

# Funktion, um das Access Token von Amadeus zu erhalten
def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")

@app.route("/flights", methods=["GET"])
def search_flights():
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    departure_date = request.args.get("departure")
    adults = request.args.get("adults", 1)

    if not origin or not destination or not departure_date:
        return jsonify({"error": "Fehlende Parameter!"}), 400

    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "max": 5
    }
    response = requests.get("https://test.api.amadeus.com/v2/shopping/flight-offers", headers=headers, params=params)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
