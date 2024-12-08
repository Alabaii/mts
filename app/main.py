from fastapi import FastAPI

from app.faults.router import router as router_faults


app = FastAPI(
    title="Мониторинг ошибок",
    version="0.1.0",
    root_path="/api",
)

app.include_router(router_faults)

@app.get("/")
async def root():
    return {"message": "Привет, мир"}