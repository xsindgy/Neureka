from fastapi import FastAPI
from database import base, db
from models.deck import Deck
from models.card import Card
from models.review import Review
from contextlib import asynccontextmanager
from routes.deck_routes import deck_router
from routes.card_routes import card_router
from routes.session_routes import session_router

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    base.metadata.create_all(bind=db)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(deck_router)
app.include_router(card_router)
app.include_router(session_router)
