import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.faults.router import router as router_faults
from starlette.middleware.base import BaseHTTPMiddleware

from app.faults.schemas import DictValidation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Мониторинг ошибок",
    version="0.1.0",
    root_path="/api",
)

origins = [
    # 3000 - порт, на котором работает фронтенд на React.js 
    "http://localhost",
]
# Настроим CORS с разрешением только стандартных заголовков
# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["Content-Type", "Authorization"],  # Разрешаем только эти заголовки
)

# Middleware для проверки заголовков
# class BlockNonStandardHeadersMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         try:
#             # Список разрешённых заголовков
#             allowed_headers = [
#                 "content-type", "content-length","authorization", "cache-control", "postman-token", 
#                 "host", "user-agent", "accept", "accept-encoding", "connection",
#             ]

#             # Проверяем все заголовки запроса
#             for header in request.headers:
#                 if header.lower() not in allowed_headers:
#                     logger.error(f"Invalid header detected: {header}")  # Логируем ошибку
#                     raise HTTPException(status_code=400, detail=f"Invalid header: {header}")

#             # Если все заголовки корректны, продолжаем выполнение запроса
#             response = await call_next(request)
#             return response

#         except HTTPException as e:
#             # Логируем исключение, которое будет обработано FastAPI
#             logger.exception(f"Invalid header error: {e.detail}")
#             # Возвращаем ошибку, она будет обработана FastAPI
#             return JSONResponse(
#                 status_code=e.status_code,
#                 content={"detail": e.detail}
#             )



# # Добавляем наш middleware в приложение
# app.add_middleware(BlockNonStandardHeadersMiddleware)


# Обработка ошибок HTTPException на уровне FastAPI
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     # Логируем ошибку HTTPException
#     logger.error(f"HTTP error occurred: {exc.detail}")
#     # Возвращаем ошибку с нужным статусом и подробностями
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.detail}
#     )



app.include_router(router_faults)



