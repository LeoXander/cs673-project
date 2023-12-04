from fastapi import FastAPI
from report_api.routers import demographic_chart

app = FastAPI()
app.include_router(demographic_chart.router)