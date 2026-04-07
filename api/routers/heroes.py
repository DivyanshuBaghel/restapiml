"""
Heroes router — list, search, and retrieve hero data.
"""

from fastapi import APIRouter, HTTPException, Query
from api.database import get_db

router = APIRouter(prefix="/api/v1/heroes", tags=["Heroes"])

# Fields returned in the lightweight list view (not the full 40KB doc)
_LIST_PROJECTION = {
    "_id": 0,
    "id": 1,
    "name": 1,
    "slug": 1,
    "role": 1,
    "specialty": 1,
    "lane": 1,
    "images.portrait": 1,
    "stats": 1,
}

# Exclude MongoDB's internal _id from detail responses
_DETAIL_PROJECTION = {"_id": 0}


@router.get("")
async def list_heroes(
    role: str | None = Query(None, description="Filter by role (e.g. Marksman, Tank, Mage)"),
    lane: str | None = Query(None, description="Filter by lane (e.g. Gold Lane, EXP Lane)"),
    name: str | None = Query(None, description="Search by hero name (case-insensitive partial match)"),
    skip: int = Query(0, ge=0, description="Number of documents to skip"),
    limit: int = Query(20, ge=1, le=132, description="Max documents to return"),
):
    """
    List all heroes with lightweight summaries.
    Supports filtering by role, lane, and name search.
    """
    db = get_db()
    query: dict = {}

    if role:
        query["role"] = {"$regex": role, "$options": "i"}
    if lane:
        query["lane"] = {"$regex": lane, "$options": "i"}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    cursor = db.heroes.find(query, _LIST_PROJECTION).skip(skip).limit(limit).sort("id", 1)
    heroes = await cursor.to_list(length=limit)
    total = await db.heroes.count_documents(query)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": heroes,
    }


@router.get("/{hero_id}")
async def get_hero_by_id(hero_id: int):
    """Get full hero document by numeric ID (handles both int and string types)."""
    db = get_db()
    
    # Try finding the hero ID as an integer, or as a string if the DB stored it that way
    hero = await db.heroes.find_one({"$or": [{"id": hero_id}, {"id": str(hero_id)}]}, _DETAIL_PROJECTION)
    
    if not hero:
        raise HTTPException(status_code=404, detail=f"Hero with id {hero_id} not found")
    return hero


@router.get("/slug/{slug}")
async def get_hero_by_slug(slug: str):
    """Get full hero document by URL-friendly slug."""
    db = get_db()
    hero = await db.heroes.find_one({"slug": slug.lower()}, _DETAIL_PROJECTION)
    if not hero:
        raise HTTPException(status_code=404, detail=f"Hero with slug '{slug}' not found")
    return hero
