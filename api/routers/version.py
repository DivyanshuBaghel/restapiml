"""
Version / app metadata router — for client update checks.
"""

from fastapi import APIRouter
from api.database import get_db

router = APIRouter(prefix="/api/v1/version", tags=["Version"])

_PROJECTION = {"_id": 0}


@router.get("")
async def get_version():
    """
    Get app metadata and data version info.
    Android clients should call this on startup to check
    if their cached data needs refreshing.
    """
    db = get_db()
    meta = await db.app_metadata.find_one({"type": "data_version"}, _PROJECTION)
    if not meta:
        return {"version": 0, "message": "No metadata found"}
    return meta
