from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse




app = FastAPI()


@app.get('/')
async def get():
    return FileResponse("app/static/index.html")



class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection.send_json(message)

        
manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await manager.connect(websocket)

    try:
        while True:
            
            data = await websocket.receive_json()

            user_message = data.get("text")
            full_message = {
                "type": 'message',
                'text': user_message
            }
            await manager.broadcast(full_message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Клиент отключился")
