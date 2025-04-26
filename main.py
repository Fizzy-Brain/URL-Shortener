from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db_connection import engine, db_ok, Base
from schema import tab
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def url_shorting(url):
    short_url = ''.join(random.choice(url) for i in range(6))
    return short_url
    

@app.post("/shorten")
def shorten_url(url : str, db: Session = Depends(db_ok)):
    existing_url = db.query(tab).filter(tab.actual_url == url).first()
    if not existing_url:
        new_url = tab(actual_url=url, short_url=url_shorting(url))
        db.add(new_url)
        db.commit()
        db.refresh(new_url)
        return {"message": "URL shortened successfully", "short_url": "http://127.0.0.1:8000/"+new_url.short_url}
    else:
        return {"message": "URL already exists", "short_url": existing_url.short_url}

@app.get("/{short_url}")
def redirect_url(short_url: str, db: Session = Depends(db_ok)):
    url = db.query(tab).filter(tab.short_url == short_url).first()
    if url:
        return RedirectResponse(url.actual_url)
    else:
        return {"message": "URL not found"}