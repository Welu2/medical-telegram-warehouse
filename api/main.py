from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from api.database import get_db
from api import crud

app = FastAPI(
    title="Medical Telegram Warehouse API",
    description="Analytical API built on dbt warehouse",
    version="1.0"
)


@app.get("/")
def home():
    return {"message": "Medical Warehouse API Running"}


# Endpoint 1
@app.get("/api/reports/top-products")
def top_products(limit: int = 10, db: Session = Depends(get_db)):

    data = crud.get_top_products(db, limit)

    return [
        {
            "product": r[0],
            "mentions": r[1]
        }
        for r in data
    ]

# Endpoint 2
@app.get(
    "/api/channels/{channel_name}/activity",
    summary="Channel activity"
)
def activity(
        channel_name: str,
        db: Session = Depends(get_db)
):

    data = crud.get_channel_activity(db, channel_name)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    return [
        {
            "channel_name": r[0],
            "date": str(r[1]),
            "posts": r[2]
        }
        for r in data
    ]


# Endpoint 3
@app.get(
    "/api/search/messages",
    summary="Search messages"
)
def search(
        query: str,
        limit: int = 20,
        db: Session = Depends(get_db)
):

    data = crud.search_messages(db, query, limit)

    return [
        {
            "message_id": r[0],
            "channel_name": r[1],
            "message": r[2],
            "date": str(r[3])
        }
        for r in data
    ]


# Endpoint 4

@app.get(
    "/api/reports/visual-content",
    summary="Visual content statistics"
)
def visual(db: Session = Depends(get_db)):

    data = crud.visual_stats(db)

    return [
        {
            "channel_name": r[0],
            "total_images": r[1],
            "average_confidence": float(r[2]) if r[2] is not None else 0
        }
        for r in data
    ]