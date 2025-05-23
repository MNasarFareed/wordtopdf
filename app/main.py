from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.router import router as word_router

app = FastAPI(title="Word to PDF Converter")

app.include_router(word_router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
