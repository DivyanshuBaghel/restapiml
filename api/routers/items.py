"""
Items router — list and retrieve game item data.
"""

from fastapi import APIRouter, HTTPException, Query
from api.database import get_db

router = APIRouter(prefix="/api/v1/items", tags=["Items"])

_PROJECTION = {"_id": 0}


@router.get("")
async def list_items(
    category: str | None = Query(None, description="Filter by item_category (e.g. Attack, Magic, Defense)"),
    tier: str | None = Query(None, description="Filter by item_tier (e.g. 1, 2, 3)"),
    name: str | None = Query(None, description="Search by item name (case-insensitive partial match)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    """
    List all items. Supports filtering by category, tier, and name search.
    """
    db = get_db()
    query: dict = {}

    if category:
        query["item_category"] = {"$regex": category, "$options": "i"}
    if tier:
        # DB might have stored tier as string or int
        try:
            tier_int = int(tier)
            query["item_tier"] = {"$in": [tier, tier_int, str(tier)]}
        except ValueError:
            query["item_tier"] = tier
    if name:
        query["item_name"] = {"$regex": name, "$options": "i"}

    cursor = db.items.find(query, _PROJECTION).skip(skip).limit(limit).sort("item_id", 1)
    items = await cursor.to_list(length=limit)
    total = await db.items.count_documents(query)

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": items,
    }


@router.get("/{item_id}")
async def get_item(item_id: str):
    """Get a single item by its item_id (e.g. 'a001')."""
    db = get_db()
    
    # Try querying as string or int to bypass MongoDB strict typing
    or_query = [{"item_id": item_id}, {"item_id": str(item_id)}]
    try:
        or_query.append({"item_id": int(item_id)})
    except ValueError:
        pass

    item = await db.items.find_one({"$or": or_query}, _PROJECTION)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item with id '{item_id}' not found")
    return item
