from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routes.product_routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
async def startup_message():
    print("🚀 FastAPI server is running!")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

