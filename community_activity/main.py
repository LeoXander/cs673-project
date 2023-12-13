import os
import sys
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
print(CURR_DIR)
sys.path.append(CURR_DIR)

db_config_dir = os.environ.get('DB_CONFIG_DIR')
db_username = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_wallet_location = os.environ.get('DB_WALLET_LOCATION')
wallet_password = os.environ.get('WALLET_PASSWORD')

def create_app():
    app = FastAPI()
    from routers import community_activity, community_activity_report, api_documentation
    from fastapi.middleware.cors import CORSMiddleware
    app.include_router(community_activity.router)
    app.include_router(community_activity_report.router)
    app.include_router(api_documentation.router)
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

app = create_app()