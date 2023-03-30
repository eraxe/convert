from fastapi import APIRouter, File, UploadFile, Form
from typing import List
from datetime import datetime
import os
from convert import components
from convert.database import SessionLocal
from convert.models import Conversion

router = APIRouter()

@router.post("/convert/txt-to-po")
async def convert_txt_to_po(user_id: int, file: UploadFile = File(...)):
    # Save the uploaded file in the appropriate directory with a unique file name
    file_dir = f"output/txt-po/{datetime.now().strftime('%Y-%m-%d')}"
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, f"{datetime.now().strftime('%H-%M-%S-%f')}-{file.filename}")
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # Convert the file and save the output in the appropriate directory with a unique file name
    po_dir = f"output/txt-po/{datetime.now().strftime('%Y-%m-%d')}"
    os.makedirs(po_dir, exist_ok=True)
    po_path = os.path.join(po_dir, f"{datetime.now().strftime('%H-%M-%S-%f')}-{file.filename.split('.')[0]}.po")
    components.txt_to_po(file_path, po_path)

    # Save the conversion information in the database
    db = SessionLocal()
    conversion = Conversion(user_id=user_id, original_file_name=file.filename, converted_file_name=os.path.basename(po_path), date=datetime.now())
    db.add(conversion)
    db.commit()
    db.refresh(conversion)
    db.close()

    return {"filename": os.path.basename(po_path)}

@router.post("/convert/po-to-txt")
async def convert_po_to_txt(user_id: int, file: UploadFile = File(...)):
    # Save the uploaded file in the appropriate directory with a unique file name
    file_dir = f"output/po-txt/{datetime.now().strftime('%Y-%m-%d')}"
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, f"{datetime.now().strftime('%H-%M-%S-%f')}-{file.filename}")
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # Convert the file and save the output in the appropriate directory with a unique file name
    txt_dir = f"output/po-txt/{datetime.now().strftime('%Y-%m-%d')}"
    os.makedirs(txt_dir, exist_ok=True)
    txt_path = os.path.join(txt_dir, f"{datetime.now().strftime('%H-%M-%S-%f')}-{file.filename.split('.')[0]}.txt")
    components.po_to_txt(file_path, txt_path)

    # Save the conversion information in the database
    db = SessionLocal()
    conversion = Conversion(user_id=user_id, original_file_name=file.filename, converted_file_name=os.path.basename(txt_path), date=datetime.now())
    db.add(conversion)
    db.commit()
    db.refresh(conversion)
    db.close()

    return {"filename": os.path.basename(txt_path)}

@router.get("/conversions/{user_id}")
async def get_user_conversions(user_id: int) -> List[Conversion]:
    db = SessionLocal()
    conversions = db.query(Conversion).filter(Conversion.user_id == user_id).all()
    db.close()
    return conversions

@router.delete("/conversion/{conversion_id}")
async def delete_conversion(conversion_id: int):
    db = SessionLocal()
    conversion = db.query(Conversion).filter(Conversion.id == conversion_id).first()
    if not conversion:
        return {"message": "Conversion not found"}
    file_path = os.path.join("output", conversion.converted_file_path)
    os.remove(file_path)
    db.delete(conversion)
    db.commit()
    db.close()
    return {"message": "Conversion deleted successfully"}
