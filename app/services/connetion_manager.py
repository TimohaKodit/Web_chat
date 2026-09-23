
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def add_user(self, websocket: WebSocket, username: str):
        self.active_connections.update({websocket: username})

        

    def disconnect(self, websocket: WebSocket):
        return self.active_connections.pop(websocket, None)

    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection.send_json(message.model_dump())
        

        
manager = ConnectionManager()
