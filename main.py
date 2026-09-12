from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
from schemas import ShortenRequest, ShortenResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Shortly")
BASE_URL = "http://127.0.0.1:8000"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/shorten", response_model=ShortenResponse, status_code=201)
def shorten(payload: ShortenRequest, db: Session = Depends(get_db)):
    url = models.Url(slug="", long_url=str(payload.long_url))
    db.add(url)
    db.flush()                    # assigns id without committing
    url.slug = str(url.id)
    db.commit()
    db.refresh(url)
    return ShortenResponse(
        slug=url.slug,
        short_url=f"{BASE_URL}/{url.slug}",
        long_url=url.long_url,
    )


@app.get("/{slug}")
def redirect(slug: str, db: Session = Depends(get_db)):
    url = db.query(models.Url).filter(models.Url.slug == slug).first()
    if url is None:
        raise HTTPException(status_code=404, detail="Not found")
    return RedirectResponse(url=url.long_url, status_code=302)