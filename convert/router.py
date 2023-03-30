from fastapi import APIRouter, Depends, UploadFile, File, Response
import shutil
import time
from fastapi import APIRouter, File, UploadFile

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



@router.post("/po-to-txt/")
async def convert_po_to_txt(po_file: UploadFile = File(...)):
    txt_filepath = "converted.txt"
    with open("temp.po", "wb") as temp_file:
        temp_file.write(await po_file.read())
    po_to_txt("temp.po", txt_filepath)
    return Response(content="File converted successfully", status_code=200)
