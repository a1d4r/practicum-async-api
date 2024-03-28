from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK, summary="Проверить состояние сервиса.")
def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "OK"}, status_code=status.HTTP_200_OK)
