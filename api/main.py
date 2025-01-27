from fastapi import FastAPI
from api.routes import patient_routes
from api.db import database
from api.models.patient_model import Base
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from api.exceptions.invalid_input_exception import InvalidInputException

Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.exception_handler(ValueError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": [
                {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
                for error in exc.errors()
            ]
        },
    )

@app.exception_handler(InvalidInputException)
async def value_error_handler(request: Request, exc: InvalidInputException):
    return JSONResponse(
        status_code=400,
        content={"detail": f"Validation error: {exc}"}
    )


app.include_router(patient_routes.router)
