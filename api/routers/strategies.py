"""
Strategies router — lane guides and gameplay strategies.
"""

from fastapi import APIRouter, HTTPException
from api.database import get_db

router = APIRouter(prefix="/api/v1/strategies", tags=["Strategies"])

_PROJECTION = {"_id": 0}


@router.get("")
async def list_strategies():
    """List all lane/strategy guides."""
    db = get_db()
    cursor = db.strategies.find({}, _PROJECTION)
    strategies = await cursor.to_list(length=20)
    return {
        "total": len(strategies),
        "data": strategies,
    }


@router.get("/{lane}")
async def get_strategy_by_lane(lane: str):
    """
    Get a single strategy guide by lane name.
    Example: 'EXP Lane', 'Mid Lane', 'Gold Lane'
    """
    db = get_db()
    # Try exact match first, then case-insensitive
    strategy = await db.strategies.find_one({"lane": lane}, _PROJECTION)
    if not strategy:
        strategy = await db.strategies.find_one(
            {"lane": {"$regex": f"^{lane}$", "$options": "i"}},
            _PROJECTION,
        )
    if not strategy:
        raise HTTPException(status_code=404, detail=f"Strategy for lane '{lane}' not found")
    return strategy
