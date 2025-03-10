import os
import requests
from fastapi import FastAPI, Query
from starlette.responses import JSONResponse

app = FastAPI()

# API-Keys aus Vercel Environment Variables laden
API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")

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

@app.get("/flights")
def search_flights(
    origin: str = Query(..., description="Abflughafen-Code"),
    destination: str = Query(..., description="Zielflughafen-Code"),
    departure: str = Query(..., description="Abflugdatum (YYYY-MM-DD)"),
    adults: int = Query(1, description="Anzahl der Erwachsenen")
):
    if not origin or not destination or not departure:
        return JSONResponse(content={"error": "Fehlende Parameter!"}, status_code=400)

    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure,
        "adults": adults,
        "max": 5
    }
    response = requests.get("https://test.api.amadeus.com/v2/shopping/flight-offers", headers=headers, params=params)
    
    return response.json()

