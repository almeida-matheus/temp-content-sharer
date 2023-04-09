from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.v1 import share_text as sharer_text_v1
from routers.v1 import share_file as sharer_file_v1
from config import ORIGINS
import logging

logging.basicConfig(level=logging.WARNING, format='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

app = FastAPI(
    title="Sharer",
    description="Temporary Content Sharer",
    version="v1",
    openapi_url='/api/sharer/v1/openapi',
    docs_url='/api/sharer/v1/swagger'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sharer_text_v1.router, prefix="/api/sharer/v1", tags=["text"])
app.include_router(sharer_file_v1.router, prefix="/api/sharer/v1", tags=["file"])