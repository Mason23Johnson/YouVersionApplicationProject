import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app import service
from app.errors import ApiError

app = FastAPI()


@app.exception_handler(ApiError)
def handle_api_error(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.get("/votd")
def votd(day: int, version: int):
    if not 1 <= day <= 366:
        raise ApiError(400, "INVALID_DAY", "day must be an integer between 1 and 366")

    try:
        return service.get_verse_of_the_day(day, version)
    except httpx.HTTPError:
        raise ApiError(502, "UPSTREAM_ERROR", "failed to reach YouVersion API")