import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Config(BaseModel):
    name: str
    value: str

app = FastAPI()
VERSION = "1.0.0"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
configs = []

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/version")
async def version():
    return {"version": VERSION}

@app.get("/env")
async def env():
    return {"environment": ENVIRONMENT}

@app.post("/config")
async def config(config: Config):
    configs.append(config)
    return config

@app.get("/config/{name}")
async def get_config(name: str):
    for cfg in configs:
        if cfg.name == name:
            return cfg
    raise HTTPException(status_code=404, detail="Config not found")

@app.delete("/config/{name}")
async def delete_config(name: str):
    for i, cfg in enumerate(configs):
        if cfg.name == name:
            del configs[i]
            return {"deleted": True}
    raise HTTPException(status_code=404, detail="Config not found")
