from fastapi import FastAPI, Request
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
def get_entries(request: Request):
    draw = int(request.query_params.get("draw", 1))
    start = int(request.query_params.get("start", 0))
    length = int(request.query_params.get("length", 25))
    search_value = request.query_params.get("search[value]", "")
    order_col = request.query_params.get("order[0][column]", None)
    order_dir = request.query_params.get("order[0][dir]", "desc")
    matches_only = request.query_params.get("matches_only") == "1"

    session = Session()
    query = session.query(Entry)
    if matches_only:
        query = query.filter_by(is_match=True)
    # Filtering
    if search_value:
        from sqlalchemy import or_
        query = query.filter(
            or_(
                Entry.title.ilike(f"%{search_value}%"),
                Entry.location.ilike(f"%{search_value}%"),
                Entry.building_type.ilike(f"%{search_value}%"),
                Entry.street.ilike(f"%{search_value}%")
            )
        )
    # Ordering
    columns = [
        Entry.id, Entry.title, Entry.link, Entry.published, Entry.location, Entry.building_type,
        Entry.rooms, Entry.floor, Entry.area, Entry.price, Entry.price_m2, Entry.street, Entry.is_match
    ]
    if order_col is not None:
        col_idx = int(order_col)
        if 0 <= col_idx < len(columns):
            col = columns[col_idx]
            if order_dir == "desc":
                col = col.desc()
            query = query.order_by(col)
    else:
        query = query.order_by(Entry.published.desc())
    total_count = session.query(Entry).count() if not matches_only else session.query(Entry).filter_by(is_match=True).count()
    filtered_count = query.count()
    entries = query.offset(start).limit(length).all()
    session.close()
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
    return JSONResponse(content={
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filtered_count,
        "data": jsonable_encoder(data)
    })

@app.get("/", response_class=HTMLResponse)
def index():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)
