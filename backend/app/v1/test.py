# pip
from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/ping",
    tags=["Test"],
)


@router.get("/", status_code=200)
def ping():
    return JSONResponse(content={"details":"Sucess"})
