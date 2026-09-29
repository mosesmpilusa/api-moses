from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(
    title="Clinical Labs & Daily Progress API",
    description="Backend service for tracking client metrics and progress logs",
    version="1.0.0",
    docs_url="/docs"
)

# In-memory database
clients_db: Dict[str, dict] = {}

# Pydantic Schemas
class MetricLog(BaseModel):
    metric_type: str  # e.g., HbA1c, Fasting Blood Glucose, BP
    value: str

class ProgressLog(BaseModel):
    weight_kg: float
    calories: int
    steps: int
    sleep_hours: float

# Endpoints
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "online", "message": "Clinical Progress API Running..."}

@app.post("/api/v1/clients/{client_id}/metrics", tags=["Clinical Labs & Progress"])
def log_metric(client_id: str, data: MetricLog):
    if client_id not in clients_db:
        clients_db[client_id] = {"metrics": [], "progress": []}
    clients_db[client_id]["metrics"].append(data.model_dump())
    return {"message": "Metric logged successfully", "metrics": clients_db[client_id]["metrics"]}

@app.get("/api/v1/clients/{client_id}/metrics", tags=["Clinical Labs & Progress"])
def get_metrics(client_id: str):
    if client_id not in clients_db:
        raise HTTPException(status_code=404, detail="Client record not found")
    return clients_db[client_id].get("metrics", [])

@app.post("/api/v1/clients/{client_id}/progress", tags=["Clinical Labs & Progress"])
def log_progress(client_id: str, data: ProgressLog):
    if client_id not in clients_db:
        clients_db[client_id] = {"metrics": [], "progress": []}
    clients_db[client_id]["progress"].append(data.model_dump())
    return {"message": "Progress entry saved", "progress": clients_db[client_id]["progress"]}

@app.get("/api/v1/clients/{client_id}/progress", tags=["Clinical Labs & Progress"])
def get_progress(client_id: str):
    if client_id not in clients_db:
        raise HTTPException(status_code=404, detail="Client record not found")
    return clients_db[client_id].get("progress", [])