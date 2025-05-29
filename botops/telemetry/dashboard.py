from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

from .db import SessionLocal, HealthCheck
import psutil

app = FastAPI()
templates = Jinja2Templates(directory="botops/telemetry/templates")


@app.get("/api/logs")
async def get_logs():
    db = SessionLocal()
    logs = db.query(HealthCheck).order_by(HealthCheck.timestamp.desc()).limit(10).all()
    db.close()
    return JSONResponse([
        {
            "cpu": log.cpu,
            "memory": log.memory,
            "disk": log.disk,
            "timestamp": log.timestamp.isoformat()
        } for log in logs
    ])
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    db = SessionLocal()
    health = HealthCheck(cpu=cpu, memory=memory, disk=disk)
    db.add(health)
    db.commit()
    db.close()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "cpu": cpu,
        "memory": memory,
        "disk": disk
    })
