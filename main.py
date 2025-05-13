from fastapi import FastAPI
from app.api.router import router

app = FastAPI(
    title="Word to PDF Converter API",
    description="API for converting Word documents to PDF format.",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")