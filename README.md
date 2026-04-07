# MLBB Guide REST API

A scalable and modern REST API built with FastAPI and MongoDB for serving Mobile Legends: Bang Bang (MLBB) game data, including heroes, items, and strategy guides.

## Tech Stack
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Database:** [MongoDB Atlas](https://www.mongodb.com/atlas)
* **Async Engine:** Motor + Uvicorn
* **Deployment IAC:** render.yaml

## Features
* Fast and fully asynchronous endpoints.
* Filterable requests for MLBB Heroes (roles, lanes, stats, name-search).
* Simple, robust error handling and pagination system.
* Automated API Documentation via Swagger/OpenAPI (`/docs`).

## Local Development

### Prerequisites
* Python 3.10+
* A live MongoDB cluster connection string.

### Setup
1. **Clone the repository:**
   ```bash
   git clone git@github.com:DivyanshuBaghel/restapiml.git
   cd restapiml
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables:**
   Create a `.env` file in the root directory with your MongoDB credentials:
   ```env
   MONGO_URI="mongodb+srv://<username>:<password>@cluster0.mongodb.net/"
   DB_NAME="your_database_name"
   ```

### Running the API
Start the local development server using Uvicorn:
```bash
uvicorn api.main:app --reload
```
The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000). Interactive Swagger docs are automatically generated and available at `http://127.0.0.1:8000/docs`.

## Deployment (Render)
This repository contains a `render.yaml` Blueprint to quickly deploy to Render.com. 

1. Connect this repo to Render via **New > Blueprint**.
2. Once the service spins up, go to its **Environment** tab.
3. Manually add the `MONGO_URI` and `DB_NAME` keys with your database details.
4. Save the changes to restart the server and connect successfully to the database.
