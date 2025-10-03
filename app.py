# app.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import hashlib

from substack_api.post import Post  # from the repo's package

app = FastAPI()

class PostOut(BaseModel):
    url: str
    canonical_url: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publication: Optional[str] = None
    published_at: Optional[str] = None
    hero_image: Optional[str] = None
    html: Optional[str] = None
    text: Optional[str] = None
    sha256: Optional[str] = None
    source: str

@app.get("/post", response_model=PostOut)
def get_post(url: str = Query(...)):
    try:
        p = Post(url)  # public posts only
        md = p.get_metadata()
        html = p.get_content(as_html=True)
        text = p.get_content(as_html=False)
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest() if text else None
        return PostOut(
            url=url,
            canonical_url=md.get("canonical_url") or url,
            title=md.get("title"),
            author=md.get("author"),
            publication=md.get("publication"),
            published_at=md.get("published_at"),
            hero_image=md.get("hero_image"),
            html=html,
            text=text,
            sha256=sha,
            source="substack_api"
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch: {e}")
