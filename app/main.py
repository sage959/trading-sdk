import uuid
from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

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
    {"symbol": "INFY", "exchange": "NSE", "instrumentType": "EQUITY", "lastTradedPrice": 1500.0}
]

ORDERS = {}
TRADES = []
PORTFOLIO = {}

def place_order_logic(order_data: dict):
    if order_data["quantity"] <= 0:
        raise ValueError("Quantity must be greater than 0")

    order_id = str(uuid.uuid4())
    order_data["orderId"] = order_id
    order_data["status"] = "PLACED"

    if order_data["orderStyle"] == "MARKET":
        order_data["status"] = "EXECUTED"
        
        trade = {
            "tradeId": str(uuid.uuid4()),
            "orderId": order_id,
            "symbol": order_data["symbol"],
            "quantity": order_data["quantity"],
            "price": order_data.get("price", 0) or 100.0
        }
        TRADES.append(trade)

        symbol = order_data["symbol"]
        current = PORTFOLIO.get(symbol, {"quantity": 0, "currentValue": 0})
        
        new_qty = current["quantity"] + order_data["quantity"]
        PORTFOLIO[symbol] = {
            "symbol": symbol,
            "quantity": new_qty,
            "averagePrice": trade["price"],
            "currentValue": new_qty * trade["price"]
        }

    ORDERS[order_id] = order_data
    return order_data

app = FastAPI(title="Trading SDK API")

@app.get("/api/v1/instruments")
def get_instruments():
    return INSTRUMENTS

@app.post("/api/v1/orders")
def create_order(order: OrderRequest):
    try:
        return place_order_logic(order.dict())
    except Exception as e:
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