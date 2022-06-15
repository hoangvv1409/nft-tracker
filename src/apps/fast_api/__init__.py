import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_400_BAD_REQUEST

from src.exceptions import AppException

from .healthz import router as HealthzRouter
from .collections.collections import router as CollectionRouter
from .collections.tokens import router as TokenRouter

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger()
app = FastAPI()

app.include_router(HealthzRouter)
app.include_router(CollectionRouter)
app.include_router(TokenRouter)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def handle_app_error_handler(req: Request, err: AppException):
    return JSONResponse(
        status_code=err.http_code,
        content=jsonable_encoder(err.to_json())
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse({"data": exc.detail}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request, exc) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"data": jsonable_encoder(exc.errors())},
    )


@app.on_event("startup")
async def startup_event():
    logger.info('Start up')


@app.on_event("shutdown")
async def shutdown_event():
    logger.info('Shut down')
