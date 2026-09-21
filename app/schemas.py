from pydantic import BaseModel, Field
from typing import Literal


class StartMessage(BaseModel):
    user: str = Field(max_length=30, min_length=1)

    

class ChatMessage(BaseModel):
    
    text: str = Field(max_length=50, min_length=1)


class ErrorMessage(BaseModel):
    type: Literal['error'] = 'error'
    text: str = Field(max_length=100, min_length=5)

class SystemMessage(BaseModel):
    type: Literal['system'] = 'system'
    text: str = Field(max_length=50, min_length=1)

class Message(BaseModel):
    user: str = Field(max_length=30, min_lenght=1)
    text: str = Field(max_length=50, min_length=1)
    type: Literal['message'] = 'message'
    


