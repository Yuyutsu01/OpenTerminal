from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Mock streaming data loop
        while True:
            # Example: In the future this will pull from market_data.py
            mock_data = {
                "type": "quote",
                "symbol": "AAPL",
                "price": 150.00,
                "timestamp": "2026-05-20T12:00:00Z"
            }
            # await manager.broadcast(json.dumps(mock_data))
            # Just keeping the connection alive for now
            await asyncio.sleep(5) 
    except WebSocketDisconnect:
        manager.disconnect(websocket)
