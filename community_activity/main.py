import os
from fastapi import FastAPI
from routers import community_activity
from dotenv import load_dotenv
load_dotenv()

db_config_dir = os.environ.get('DB_CONFIG_DIR')
db_username = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_wallet_location = os.environ.get('DB_WALLET_LOCATION')
db_wallet_password = os.environ.get('DB_WALLET_PASSWORD')

app = FastAPI()

app.include_router(community_activity.router)