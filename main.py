# import uvicorn
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# from .dependencies import get_query_token, get_token_header
# from .app.routers import landing, auth, chat, users, dashboard
from app.routers import landing, auth, chat, users, dashboard
from app.config import SECRET_KEY

app = FastAPI(
    # dependencies=[Depends(get_query_token)]
)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/assets", StaticFiles(directory="app/templates/assets"), name="assets")
app.include_router(landing.router)
app.include_router(auth.router)
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(users.router)
app.include_router(dashboard.router)


# @app.get("/")
# async def root():
#     return {
#         "message": "Hello ChatBot Applications!"
#     }
