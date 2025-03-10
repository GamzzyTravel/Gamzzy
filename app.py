from fastapi import FastAPI
import requests

app = FastAPI()

# API-Keys direkt im Code (nur für Testzwecke!)
API_KEY = "NUr5GWYPyRkuieBC8locpeNUWzLL65hB"
API_SECRET = "BQyVvOw4vbsXbfxh"

# Endpunkt zum Testen
@app.get("/")
def home():
    return {"message": "Gamzzy Flight API is running!"}

# Flugsuche API
@app.get("/flights")
def get_flights(origin: str, destination: str, departure: str):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure,
        "adults": 1,
        "max": 5
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
