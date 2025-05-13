import io
import zipfile
from fastapi import HTTPException

async def validate_files(files, max_files, max_total_size_mb):
    if len(files) > max_files:
        raise HTTPException(status_code=400, detail=f"Maximum {max_files} files allowed.")
    
    total_size = 0
    for file in files:
        if not file.filename.lower().endswith((".docx", ".doc")):
            raise HTTPException(status_code=400,
                               detail={"success": False, "error": "Only DOCX or DOC files are allowed."}
)
        
        contents = await file.read()
        total_size += len(contents)
        file.file.seek(0)  # Reset file pointer after reading
    
    if total_size > max_total_size_mb * 1024 * 1024:
            raise HTTPException(status_code=400,
                                detail={"success": False, "error": f"Total files size exceeds {max_total_size_mb} MB."}
)

def create_zip_file(files_dict):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for filename, data in files_dict.items():
            zipf.writestr(filename, data)
    zip_buffer.seek(0)
    return zip_buffer
