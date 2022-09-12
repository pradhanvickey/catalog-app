import base64
import os
import uuid
from typing import Union

import png  # noqa
import pyqrcode  # noqa
from fastapi import HTTPException
from pydantic import HttpUrl
from pyqrcode import QRCode  # noqa

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


def create_qr_code_url(unique_store_key):
    s = f"{settings.BASE_URL}/store/{unique_store_key}"
    url = pyqrcode.create(s)
    path = os.path.join(TEMP_FILE_FOLDER, unique_store_key)
    url.png(path, scale=6)
    url = s3.upload_photo(path, unique_store_key, ".png")
    os.remove(path)
    return url
