from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from json import JSONDecodeError



app = FastAPI()


@app.get('/')
async def get():
    return FileResponse("app/static/index.html")



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
            await connection.send_json(message)
        

        
manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await manager.connect(websocket)
    try:
        data = await websocket.receive_json()
        username = data.get("user")
        if username:

            manager.add_user(websocket, username)
            message_auth = {
                "type": "system",
                "text": f"{username} вошел в чат!"
            }
            await manager.broadcast(message_auth)
        else:
            await websocket.close()
            return 
             
             

    
        
        while True:
                data = await websocket.receive_json()
            

                user_message = data.get("text")
            
                full_message = {
                "type": 'message',
                "user": username,
                'text': user_message
                }
                await manager.broadcast(full_message)
    except WebSocketDisconnect:
            username = manager.disconnect(websocket)
            if username:
                await manager.broadcast({"type": "system", "text": f"{username} вышел из чата."})
    except JSONDecodeError:
        await websocket.close()
        username = manager.disconnect(websocket)
        if username:
            await manager.broadcast({"type": "system", "text": f"{username} вышел из чата."})