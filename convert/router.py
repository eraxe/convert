from fastapi import APIRouter, File, UploadFile, Response
import shutil
import time

from .components import po_to_txt
from .components import txt_to_po

router = APIRouter()

@router.post("/convert/txt-to-po", status_code=200)
async def convert_txt_to_po(txt_file: UploadFile = File(...)):
    po_filepath = f"output/output-{int(time.time())}.po"

    with open("temp.txt", "wb") as buffer:
        shutil.copyfileobj(txt_file.file, buffer)

    txt_to_po("temp.txt", po_filepath)
    return {"detail": "File converted successfully", "output_path": po_filepath}


@router.post("/convert/po-to-txt", status_code=200)
async def convert_po_to_txt(po_file: UploadFile = File(...)):
    txt_filepath = "converted.txt"
    with open("temp.po", "wb") as temp_file:
        shutil.copyfileobj(po_file.file, temp_file)
    po_to_txt("temp.po", txt_filepath)
    with open(txt_filepath, "r") as txt_file:
        content = txt_file.read()
    return Response(content=content, media_type="text/plain")

