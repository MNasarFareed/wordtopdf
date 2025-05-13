from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.services.converter import convert_word_file
from app.utils.file_handler import validate_files, create_zip_file
from app.auth.auth_handler import verify_api_key
import io
import asyncio

router = APIRouter(prefix="/word", dependencies=[Depends(verify_api_key)])

MAX_FILES = 10
MAX_TOTAL_SIZE_MB = 50

@router.post("/pdf")
async def convert_files(
    files: list[UploadFile] = File(...),
    api_key: str = Depends(verify_api_key)
):
    # Validate files
    await validate_files(files, MAX_FILES, MAX_TOTAL_SIZE_MB)

    tasks = [convert_word_file(file) for file in files]
    pdf_results = await asyncio.gather(*tasks, return_exceptions=True)

    files_dict = {}
    for file, result in zip(files, pdf_results):
        if isinstance(result, Exception):
            raise HTTPException(status_code=500,
                                detail={"success": False, "error": f"Error converting file {file.filename}: {result}"}
)

        base_name = file.filename.rsplit('.', 1)[0]
        pdf_name = f"{base_name}.pdf"
        files_dict[pdf_name] = result

    zip_buffer = create_zip_file(files_dict)
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": "attachment; filename=converted_files.zip"}
    )
