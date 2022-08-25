import base64
import os
import uuid
from typing import Union
import pyqrcode  # noqa
import png  # noqa
from pyqrcode import QRCode  # noqa
from fastapi import HTTPException
from pydantic import HttpUrl

from app.config import settings
from app.constants import TEMP_FILE_FOLDER
from app.utils.s3_util import s3


def decode_photo(path, encoded_string):
    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encoded_string.encode("utf-8")))
        except Exception as ex:
            raise HTTPException(status_code=400, detail="Invalid photo encoding")


def upload_photo_to_s3(encoded_photo: Union[str, bytes], ext: str) -> HttpUrl:
    name = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(TEMP_FILE_FOLDER, name)
    decode_photo(path, encoded_photo)
    url = s3.upload_photo(path, name, ext)
    os.remove(path)
    return url


def create_qr_code_url(store_name):
    s = f"{settings.BASE_URL}/store/{store_name}"
    url = pyqrcode.create(s)
    path = os.path.join(TEMP_FILE_FOLDER, store_name)
    url.png(path, scale=6)
    url = s3.upload_photo(path, store_name, ".png")
    os.remove(path)
    return url
