# Trading SDK

This project is a simplified trading backend that simulates core broker functionalities such as
instrument listing, order placement, trade execution, and portfolio tracking.

# Tech
- Python
- FastAPI
- Uvicorn
- Pydantic

# Features
- View tradable instruments
- Place BUY orders (MARKET)
- Track order status
- View executed trades
- Fetch portfolio holdings
- In-memory data storage

## Setup Instructions

1. Install dependencies
   pip install fastapi uvicorn pydantic

2. Run the server
   uvicorn main:app

3. Open Swagger UI
   http://127.0.0.1:8000/docs

# Assumptions
- Single hardcoded user
- Market orders execute immediately
- No real market connectivity
- In-memory storage only

# Sample APIs
- GET /api/v1/instruments
- POST /api/v1/orders
- GET /api/v1/orders/{orderId}
- GET /api/v1/trades
- GET /api/v1/portfolio
