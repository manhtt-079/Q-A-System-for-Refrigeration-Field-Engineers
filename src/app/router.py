from fastapi import APIRouter
from app.schema import ChatRequest
from app.service import oneturn_chat

qa_router = APIRouter(
    prefix='/api/qa',
    tags=['qa']
)

global chat_history
chat_history = []
@qa_router.post('/chat')
async def chat(e: ChatRequest):
    global chat_history
    response, chat_history = oneturn_chat(chat_history, e.query)
    
    return {
        "success": True,
        "message": response
    }


@qa_router.get("/")
def root():
    return {
        "success": True,
        "message": "This is qa page."
    }

if __name__=='__main__':
    pass
