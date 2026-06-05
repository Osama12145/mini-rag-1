from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
import aiofiles
from models import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')# هنا بنستخدم لوجر اليوفركورن عشان نسجل اي اخطاء ممكن تصير اثناء رفع الملفات او التعامل معها

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
        
    
    # validate the file properties
    data_controller = DataController()# عشان يستخدم الاوبجكت اللي سويناه في 
    # DataController.py عشان يقدر يستخدم الميثود اللي سويناها في DataController.py وهي validate_uploaded_file عشان يتحقق من نوع الملف وحجمه قبل ما يخزنه

    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:# هنا بنفتح الملف اللي راح نخزن فيه البيانات المرفوعة بصيغة الكتابة الثنائية "wb" لان ممكن تكون ملفات pdf او csv او غيرها من الملفات اللي تحتاج لكتابة ثنائية
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
            content={
                "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                "file_id": file_id
            }
        )
