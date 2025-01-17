from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.service.chatbotService import ChatbotService
from app.core.database import get_db

chatbotRouter = APIRouter()

@chatbotRouter.post("/chat")
def handle_query(user_query: str,db: Session = Depends(get_db)):
    return ChatbotService.process_query(user_query, db)
