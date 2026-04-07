# Using the MLBB Guide API

Welcome to the Mobile Legends: Bang Bang (MLBB) Guide REST API! This document outlines how to interact with the API to retrieve Heroes, Items, and Strategies. 

## Base URLs
* **Local Development:** `http://127.0.0.1:8000`
* **Production / Render:** (Replace with your actual Render URL when deployed)
* **Interactive Docs:** Visit `/docs` on your domain for the Swagger UI, which allows you to test out the API endpoints directly in your browser!

---

## 🦸 Heroes Endpoints

### 1. List Heroes (with filters)
**`GET /api/v1/heroes`**
Fetches a lightweight list of heroes. You can filter by role, lane, or name.

**Query Parameters:**
* `role` (str): e.g. "Marksman", "Tank"
* `lane` (str): e.g. "Gold Lane", "EXP Lane"
* `name` (str): Partial match for hero name searches
* `skip` (int): Pagination offset (default 0)
* `limit` (int): Number of returned documents (default 20)

**Example Request:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/api/v1/heroes?role=Marksman&limit=5'
```

### 2. Get Hero by ID
**`GET /api/v1/heroes/{hero_id}`**
Fetches the full JSON document (including lore, stats, and individual guides) for a specific hero using their numeric ID.

**Example Request:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/api/v1/heroes/15'
```

### 3. Get Hero by Slug
**`GET /api/v1/heroes/slug/{slug}`**
Fetches a hero by their URL-friendly, lowercase string slug name.

**Example Request:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/api/v1/heroes/slug/chou'
```

---

## 🗡️ Items Endpoints

### 1. List Items
**`GET /api/v1/items`**
Fetch a paginated list of all items across the game. 

**Query Parameters:**
* `category` (str): e.g. "Magic", "Defense", "Attack"
* `tier` (str): e.g. "1", "2", "3"
* `name` (str): Search for a specific item name.

**Example Request:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/api/v1/items?category=Defense&tier=3'
```

### 2. Get Item by ID
**`GET /api/v1/items/{item_id}`**
Fetch detailed statistics using the item's alphanumeric code.

**Example Request:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/api/v1/items/a001'
```

---

## 🗺️ Strategies Endpoints

### 1. List Strategies
**`GET /api/v1/strategies`**
List all overarching lane mapping guides and gameplay strategy data.

### 2. Get Strategy By Lane
**`GET /api/v1/strategies/{lane}`**
Retrieve a specific strategy description and objective guide for the provided lane.

**Example Request:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/api/v1/strategies/EXP%20Lane'
```

---

## Example Data Structure
When requesting `GET /api/v1/heroes?name=Alucard`, expect a structured JSON envelope containing metadata and the respective documents:

```json
{
  "total": 1,
  "skip": 0,
  "limit": 20,
  "data": [
    {
      "id": 7,
      "name": "Alucard",
      "slug": "alucard",
      "role": "Fighter / Assassin",
      "specialty": "Chase / Damage",
      "lane": "EXP Lane / Jungler",
      "stats": {},
      "images": {}
    }
  ]
}
```
