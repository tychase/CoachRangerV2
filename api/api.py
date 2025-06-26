from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from typing import Optional

app = FastAPI(title="CoachRanger API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Listing(BaseModel):
    title: str
    detail_url: str
    price: int
    year: Optional[int] = None
    model: Optional[str] = None
    slides: Optional[int] = 0
    converter: Optional[str] = None
    featured_image: Optional[str] = None

def load_data():
    with open("scraper/listings.json") as f:
        return [Listing(**item) for item in json.load(f)]

@app.get("/listings", response_model=list[Listing])
def get_listings(sort: str = "price", dir: str = "desc"):
    data = load_data()
    reverse = dir == "desc"
    if hasattr(Listing, sort):
        data.sort(key=lambda x: getattr(x, sort) or 0, reverse=reverse)
    return data

@app.get("/search", response_model=list[Listing])
def search_listings(
    q: str = Query(..., min_length=2),
    sort: str = "price",
    dir: str = "desc"
):
    data = load_data()
    q_lower = q.lower()
    filtered = [
        l for l in data
        if q_lower in l.title.lower() or
           (l.model and q_lower in l.model.lower()) or
           (l.converter and q_lower in l.converter.lower())
    ]
    reverse = dir == "desc"
    if hasattr(Listing, sort):
        filtered.sort(key=lambda x: getattr(x, sort) or 0, reverse=reverse)
    return filtered