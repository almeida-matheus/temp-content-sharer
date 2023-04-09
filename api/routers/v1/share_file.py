from fastapi import APIRouter, HTTPException
from typing import Optional
from providers.aws import S3
from models.sharer import FilePostResponse, FileGetRequest, SharerResponse
from utils.tools import get_random_id
import logging

router = APIRouter()
logging.getLogger(__name__)
s3 = S3()

@router.get("/upload/file")
async def get_url_to_upload_file(name: Optional[str] = None, extension: Optional[str] = None) -> FilePostResponse:
    ''' return a pre-signed URL from s3 for direct file upload using POST request'''
    try:
        if name:
            object_key = name
        else:
            random_id = get_random_id(16)
            object_key = random_id
            if extension:
                object_key += extension
        presigned_url_post = s3.generate_presigned_post(object_key)
        return FilePostResponse(url=presigned_url_post['url'],fields=presigned_url_post['fields'])
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/upload/file")
async def read_existent_s3_object(req: FileGetRequest) -> SharerResponse:
    ''' return a pre-signed URL of an S3 object for temporary download based on key object '''
    try:
        presigned_url = s3.generate_presigned_url(req.name, req.expiration)
        return SharerResponse(temporary_url=presigned_url)
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))
