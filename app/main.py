import uuid
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

class OrderRequest(BaseModel):
    symbol: str
    quantity: int
    orderStyle: str
    price: Optional[float] = None
    action: str = "BUY"

INSTRUMENTS = [
    {"symbol": "BAJAJ-AUTO", "exchange": "NSE", "instrumentType": "EQUITY", "lastTradedPrice": 4500.0},
    {"symbol": "RELIANCE", "exchange": "NSE", "instrumentType": "EQUITY", "lastTradedPrice": 2400.0},
    {"symbol": "TCS", "exchange": "NSE", "instrumentType": "EQUITY", "lastTradedPrice": 3500.0},
    {"symbol": "INFY", "exchange": "NSE", "instrumentType": "EQUITY", "lastTradedPrice": 1500.0},
    {"symbol": "HDFCBANK", "exchange": "NSE", "instrumentType": "EQUITY", "lastTradedPrice": 1620.0},
    {"symbol": "WIPRO", "exchange": "NSE", "instrumentType": "EQUITY", "lastTradedPrice": 480.0},
    {"symbol": "TESLA", "exchange": "NASDAQ", "instrumentType": "EQUITY", "lastTradedPrice": 175.0},
    {"symbol": "APPLE", "exchange": "NASDAQ", "instrumentType": "EQUITY", "lastTradedPrice": 189.0},
    {"symbol": "GOOGLE", "exchange": "NASDAQ", "instrumentType": "EQUITY", "lastTradedPrice": 141.0},
    {"symbol": "MICROSOFT", "exchange": "NASDAQ", "instrumentType": "EQUITY", "lastTradedPrice": 415.0},
]

ORDERS = {}
TRADES = []
PORTFOLIO = {}

def place_order_logic(order_data: dict):
    if order_data["quantity"] <= 0:
        raise ValueError("Quantity must be greater than 0")

    symbol = order_data["symbol"]
    action = order_data.get("action", "BUY")
    current = PORTFOLIO.get(symbol, {"quantity": 0, "currentValue": 0, "averagePrice": 0})

    if action == "SELL" and current["quantity"] < order_data["quantity"]:
        raise ValueError(f"Not enough shares to sell. You hold {current['quantity']} shares of {symbol}.")

    order_id = str(uuid.uuid4())
    order_data["orderId"] = order_id
    order_data["status"] = "PLACED"

    if order_data["orderStyle"] == "MARKET":
        order_data["status"] = "EXECUTED"

    instrument = next((i for i in INSTRUMENTS if i["symbol"] == symbol), None)
    trade_price = order_data.get("price") or (instrument["lastTradedPrice"] if instrument else 100.0)

    trade = {
        "tradeId": str(uuid.uuid4()),
        "orderId": order_id,
        "symbol": symbol,
        "quantity": order_data["quantity"],
        "price": trade_price,
        "action": action
    }
    TRADES.append(trade)

    if action == "SELL":
        new_qty = current["quantity"] - order_data["quantity"]
    else:
        new_qty = current["quantity"] + order_data["quantity"]

    if new_qty == 0:
        PORTFOLIO.pop(symbol, None)
    else:
        PORTFOLIO[symbol] = {
            "symbol": symbol,
            "quantity": new_qty,
            "averagePrice": trade_price,
            "currentValue": round(new_qty * trade_price, 2)
        }

    ORDERS[order_id] = order_data
    return order_data

app = FastAPI(title="Trading SDK API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")

@app.get("/api/v1/instruments")
def get_instruments():
    return INSTRUMENTS

@app.get("/api/v1/orders")
def get_all_orders():
    return list(ORDERS.values())

@app.post("/api/v1/orders")
def create_order(order: OrderRequest):
    try:
        return place_order_logic(order.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in ORDERS:
        raise HTTPException(status_code=404, detail="Order not found")
    return ORDERS[order_id]

@app.get("/api/v1/trades")
def get_trades():
    return TRADES

@app.get("/api/v1/portfolio")
def get_portfolio():
    return list(PORTFOLIO.values())