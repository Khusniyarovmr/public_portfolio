import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, PlainTextResponse

from api.v1 import base
from core.config import app_settings
from services.logger.logger import logger

# Инициализация объекта приложения
app = FastAPI(
    title=app_settings.app_title,  # название приложение берём из настроек
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello, World!!!"


app.include_router(base.api_router, prefix='/api/v1')

if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    logger.info('Start application')
    uvicorn.run(
        'main:app',
        host=app_settings.PROJECT_HOST,
        port=app_settings.PROJECT_PORT,
        reload=True
    )
