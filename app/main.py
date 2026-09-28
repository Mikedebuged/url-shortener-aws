import logging
import secrets

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("shortener")

app = FastAPI(title="URL Shortener")

# In-memory storage for now. Swapped for DynamoDB later.
urls: dict[str, str] = {}


class ShortenRequest(BaseModel):
    url: HttpUrl


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/shorten", status_code=201)
def shorten(req: ShortenRequest):
    code = secrets.token_urlsafe(4)
    while code in urls:
        code = secrets.token_urlsafe(4)
    urls[code] = str(req.url)
    logger.info("created code=%s url=%s", code, req.url)
    return {"code": code, "short_url": f"/{code}"}


@app.get("/{code}")
def redirect(code: str):
    target = urls.get(code)
    if target is None:
        logger.warning("miss code=%s", code)
        raise HTTPException(status_code=404, detail="Code not found")
    logger.info("hit code=%s", code)
    return RedirectResponse(target, status_code=307)