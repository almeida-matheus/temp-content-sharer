from fastapi import APIRouter, HTTPException
from providers.aws import S3
from models.sharer import TextRequest, SharerResponse
from utils.tools import get_random_id
import logging

router = APIRouter()
logging.getLogger(__name__)
s3 = S3()

@router.post("/upload/text")
async def create_new_s3_object(req: TextRequest) -> SharerResponse:
    ''' return a pre-signed URL of a new object in S3 for temporary download based on a text content '''
    try:
        if req.name:
            object_key = req.name
        else:
            random_id = get_random_id(16)
            object_key = random_id + req.extension
        s3.put_object(object_key, req.text)
        presigned_url = s3.generate_presigned_url(object_key, req.expiration)
        return SharerResponse(temporary_url=presigned_url)
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=404, detail=str(e))