from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.connetion_manager import manager
from app.schemas import StartMessage, ChatMessage, SystemMessage, ErrorMessage, Message
from pydantic import ValidationError
from json import JSONDecodeError

router_ws = APIRouter()


@router_ws.websocket("/ws")
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
