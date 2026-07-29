# FastAPI Fruit Management API

A lightweight RESTful API built with Python and FastAPI for managing fruit inventory. Includes automatic data validation via Pydantic and interactive OpenAPI documentation.

## Features
- **GET `/fruits`**: Retrieve all fruit items.
- **POST `/fruits`**: Add a new fruit to the inventory.
- **GET `/fruits/{id}`**: Fetch fruit details by ID index.
- Data validation and error handling using Pydantic & HTTP Exceptions.

## Quickstart

### 1. Clone the repository & set up environment
```bash
git clone [https://github.com/your-username/fastapi-fruit-api.git](https://github.com/your-username/fastapi-fruit-api.git)
cd fastapi-fruit-api

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the server
```bash
uvicorn app.main:app --reload
```

### 3. View Interactive Documentation
Once running, navigate to:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`