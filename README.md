# Trading SDK

A simulated stock trading backend that mimics core broker functionalities such as
instrument listing, order placement, trade execution, and portfolio tracking.

🌐 Live: https://trading-sdk.onrender.com

> ⚠️ Hosted on Render free tier — first request after inactivity may take ~50 seconds.

![Trading SDK Dashboard](assets/screenshot.png)

## Tech
- Python
- FastAPI
- Uvicorn
- Pydantic
- HTML / CSS / JS (Vanilla)

## Features
- Browse 10 tradable instruments (NSE + NASDAQ)
- Place BUY / SELL orders (MARKET & LIMIT)
- Track order status with pagination
- View executed trades
- Portfolio holdings with Unrealised & Realised P&L
- Interactive price chart per stock
- In-memory data storage

## Setup

1. Install dependencies
pip install fastapi uvicorn pydantic

text

2. Run the server
uvicorn app.main:app --reload

text

3. Open in browser
http://127.0.0.1:8000

text

## API Endpoints
- GET /api/v1/instruments
- POST /api/v1/orders
- GET /api/v1/orders
- GET /api/v1/orders/{orderId}
- GET /api/v1/trades
- GET /api/v1/portfolio

## Assumptions
- Single hardcoded user
- Market orders execute immediately
- No real market connectivity
- In-memory storage only

Made with ❤️ by [Dev](https://www.instagram.com/dev7kalra/) and [Siddharth](https://www.instagram.com/siddharthh_959/)