from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from json import JSONDecodeError
from pydantic import ValidationError
from app.schemas import StartMessage, ChatMessage, SystemMessage, ErrorMessage, Message



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
            await connection.send_json(message.model_dump())
        

        
manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await manager.connect(websocket)
    try:
        data = await websocket.receive_json()
        
        join = StartMessage.model_validate(data)
        

        manager.add_user(websocket, join.user)
        message_auth = SystemMessage(text=f"{join.user} вошел в чат!")
        await manager.broadcast(message_auth)
        
             
             

    
        
        while True:
                try:
                    data = await websocket.receive_json()
            

                    user_message = ChatMessage.model_validate(data)
                    
                    
                    mes = Message(user=join.user, text=user_message.text)
                    await manager.broadcast(mes)
                except ValidationError as e:
                    message_error = ErrorMessage(text="Message incorrect")
                    await websocket.send_json(message_error.model_dump())
                    print(e)

    except WebSocketDisconnect:
            username = manager.disconnect(websocket)
            if username:
                log_out_mes = SystemMessage(text=f'{join.user} вышел из чата')
                await manager.broadcast(log_out_mes)
    except JSONDecodeError:
        await websocket.close()
        username = manager.disconnect(websocket)
        if username:
            log_out_mes = SystemMessage(text=f'{join.user} вышел из чата')
            await manager.broadcast(log_out_mes)
    except ValidationError:
        await websocket.close()
        username = manager.disconnect(websocket)

        
