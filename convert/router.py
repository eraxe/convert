from fastapi import APIRouter, Depends, UploadFile, File, Response

from .components import po_to_txt

router = APIRouter()

@router.post("/po-to-txt/")
async def convert_po_to_txt(po_file: UploadFile = File(...)):
    txt_filepath = "converted.txt"
    with open("temp.po", "wb") as temp_file:
        temp_file.write(await po_file.read())
    po_to_txt("temp.po", txt_filepath)
    return Response(content="File converted successfully", status_code=200)
