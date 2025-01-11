from fastapi import FastAPI, Depends , HTTPException
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter 
from app.routers.admin import adminRouter
from app.util.protectRoute import get_current_user
from app.db.schema.user import UserOutput
from app.service.chatbotService import handle_query
from app.core.database import get_db
from sqlalchemy.orm import Session

@asynccontextmanager
async def lifespan(app : FastAPI):
    create_tables()
    yield 

app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")
app.include_router(router=adminRouter, tags=["admin"], prefix="/admin")

@app.post("/chatbot/")
def chatbot_endpoint(query: str, db: Session = Depends(get_db)):
    """
    Endpoint for handling chatbot queries.
    """
    print("query", query)
    response = response = handle_query(query, user_info={}, db=db)

    return response
    
@app.get("/health")
def health():
    return {"status" : "Running...."}

@app.get("/protected")
def read_protected(user : UserOutput = Depends(get_current_user)):
    return {"data" : user}
