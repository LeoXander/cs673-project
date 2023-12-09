from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
print(CURR_DIR)
sys.path.append(CURR_DIR)

def create_app():
    app = FastAPI()
    from routers import demographic_chart, servicesOffered
    app.include_router(demographic_chart.router)
    app.include_router(servicesOffered.router)
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

app = create_app()