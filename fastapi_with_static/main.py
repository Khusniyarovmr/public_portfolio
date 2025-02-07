import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.api.routes import route
from src.db.postgres import stop_engine, start_engine
from src.models import *  # noqa
from src.services.init_log_data import init_log_data


async def lifespan(app: FastAPI):
    print("Starting up...")
    try:
        await start_engine()
        await init_log_data()
    except Exception as e:
        print(f"Error during startup: {e}")
        raise

    yield
    print("Shutting down...")
    try:
        await stop_engine()
    except Exception as e:
        print(f"Application shutdown failed: {e}")


app = FastAPI(
    title='test_project',
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan
)
app.include_router(route, prefix='/api')
app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
def read_root():
    return FileResponse("static/index.html")


origins = [
    "http://0.0.0.0:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1, reload=True)
