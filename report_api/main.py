from fastapi import FastAPI
from routers import demographic_chart

app = FastAPI()

app.include_router(demographic_chart.router)