from fastapi import APIRouter, Depends, Response, Query

from .components import download_file

router = APIRouter()

@router.get("/download/")
async def download_from_url(url: str):
    local_path = "downloaded_file"
    download_file(url, local_path)
    return Response(content="File downloaded successfully", status_code=200)
