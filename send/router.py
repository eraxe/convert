from fastapi import APIRouter, Depends, UploadFile, File, Response

from .components import send_file_to_server

router = APIRouter()

@router.post("/send-to-server/")
async def send_file(server_url: str, file: UploadFile = File(...)):
    with open("tempfile", "wb") as f:
        f.write(await file.read())
    status_code = send_file_to_server("tempfile", server_url)
    return Response(content="File sent successfully", status_code=status_code)
