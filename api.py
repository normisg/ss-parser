from fastapi import FastAPI
from db_utils import Session, Entry
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
import os

app = FastAPI()

@app.get("/stats")
def get_stats():
    session = Session()
    total = session.query(Entry).count()
    matches = session.query(Entry).filter_by(is_match=True).count()
    session.close()
    return JSONResponse({"total": total, "matches": matches})

@app.get("/entries")
def get_entries():
    session = Session()
    entries = session.query(Entry).all()
    session.close()
    # Convert SQLAlchemy objects to dicts
    data = [
        {
            "id": e.id,
            "title": e.title,
            "link": e.link,
            "published": e.published,
            "is_processed": e.is_processed,
            "is_match": e.is_match,
            "location": e.location,
            "building_type": e.building_type,
            "rooms": e.rooms,
            "floor": e.floor,
            "area": e.area,
            "price": e.price,
            "price_m2": e.price_m2,
            "street": e.street
        }
        for e in entries
    ]
    return JSONResponse(content=jsonable_encoder(data))

@app.get("/", response_class=HTMLResponse)
def index():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)
