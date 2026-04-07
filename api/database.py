"""
Async MongoDB connection via Motor.
"""

from motor.motor_asyncio import AsyncIOMotorClient
import certifi

from api.config import MONGO_URI, DB_NAME

_client: AsyncIOMotorClient | None = None


def get_db():
    """Return the database handle. Call connect() first."""
    if _client is None:
        raise RuntimeError("Database not connected. Call connect() first.")
    return _client[DB_NAME]


async def connect():
    """Open the Motor client and verify the connection."""
    global _client
    _client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
    # Force a round-trip to verify credentials / network
    await _client.admin.command("ping")
    print(f"✅ Connected to MongoDB ({DB_NAME})")


async def disconnect():
    """Close the Motor client."""
    global _client
    if _client:
        _client.close()
        _client = None
        print("🔌 Disconnected from MongoDB")
