import os
from fastapi import FastAPI
from routers import community_activity
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

db_config_dir = os.environ.get('DB_CONFIG_DIR')
db_username = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_wallet_location = os.environ.get('DB_WALLET_LOCATION')
wallet_password = os.environ.get('WALLET_PASSWORD')

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(community_activity.router)