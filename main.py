from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db_connection import get_db, Base, engine
from schema import URL
from pydantic import BaseModel, HttpUrl
import secrets
import string

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A simple API to shorten long URLs",
    version="1.0.0",
)

class URLBase(BaseModel):
    original_url: HttpUrl

class URLResponse(URLBase):
    short_url: str

    class Config:
        from_attributes = True

def generate_short_url(length: int = 6) -> str:
    """Generate a random short URL."""
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

@app.post("/shorten", response_model=URLResponse)
def shorten_url(url: URLBase, db: Session = Depends(get_db)):
    """Shorten a URL."""
    short_url = generate_short_url()
    
    # Check if short URL already exists
    while db.query(URL).filter(URL.short_url == short_url).first():
        short_url = generate_short_url()
    
    db_url = URL(original_url=str(url.original_url), short_url=short_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return db_url

@app.get("/{short_url}")
def redirect_url(short_url: str, db: Session = Depends(get_db)):
    """Redirect to the original URL."""
    url = db.query(URL).filter(URL.short_url == short_url).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"original_url": url.original_url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)