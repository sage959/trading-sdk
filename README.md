# 📈 Trading SDK

A simulated stock trading backend that mimics core broker functionalities — instrument listing, order placement, trade execution, and portfolio tracking — with a clean dashboard UI.

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

**1. Install dependencies**
```bash
pip install fastapi uvicorn pydantic
```

**2. Run the server**
```bash
uvicorn app.main:app --reload
```

**3. Open in browser**
```
http://127.0.0.1:8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/instruments | List all stocks |
| POST | /api/v1/orders | Place an order |
| GET | /api/v1/orders | Get all orders |
| GET | /api/v1/orders/{orderId} | Get order by ID |
| GET | /api/v1/trades | View all trades |
| GET | /api/v1/portfolio | View holdings |

## Made with ❤️ by [Dev](https://www.instagram.com/dev7kalra/) and [Siddharth](https://www.instagram.com/siddharthh_959/)