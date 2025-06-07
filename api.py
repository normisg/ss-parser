from fastapi import FastAPI
from db_utils import Session, Entry
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/stats")
def get_stats():
    session = Session()
    total = session.query(Entry).count()
    matches = session.query(Entry).filter_by(is_match=True).count()
    session.close()
    return JSONResponse({"total": total, "matches": matches})
