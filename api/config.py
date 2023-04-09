import os

BUCKET_NAME = os.getenv('BUCKET_NAME', 'my-personal-bucket-br')
ORIGINS = os.getenv('ORIGINS', ["http://127.0.0.1:5500"])