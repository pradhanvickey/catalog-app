import os

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from app.config import settings
from app.constants import TEMP_FILE_FOLDER

AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
AWS_SECRET = settings.AWS_SECRET
AWS_BUCKET = settings.AWS_BUCKET
AWS_REGION = settings.AWS_REGION


class S3Service:
    def __init__(self):
        self.key = AWS_ACCESS_KEY
        self.secret = AWS_SECRET
        self.bucket = AWS_BUCKET
        self.s3 = boto3.client("s3", aws_access_key_id=self.key, aws_secret_access_key=self.secret, )

    def upload_photo(self, path, key, ext):
        try:
            self.s3.upload_file(path, self.bucket, key,
                                ExtraArgs={'ACL': 'public-read', 'ContentType': f'image / {ext}'})
            return f"https://{AWS_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{key}"
        except ClientError as ex:
            raise HTTPException(status_code=500, detail="S3 is not available at the moment")
        except Exception as ex:
            raise HTTPException(status_code=500, detail="S3 is not available at the moment")

    def download_photo(self, key):
        file_name = os.path.join(TEMP_FILE_FOLDER, key)
        self.s3.download_file(
            Bucket=self.bucket, Key=key, Filename=file_name
        )
        return file_name


s3 = S3Service()
