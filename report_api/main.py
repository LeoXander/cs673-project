from fastapi import FastAPI
import os
import sys
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
print(CURR_DIR)
sys.path.append(CURR_DIR)

def create_app():
    app = FastAPI()
    from routers import demographic_chart
    app.include_router(demographic_chart.router)
    return app

app = create_app()

