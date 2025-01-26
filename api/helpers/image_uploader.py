from fastapi import UploadFile
import os
import shutil

def upload_image(image: UploadFile):
    directory = "images"
    os.makedirs(directory, exist_ok=True)
    image_path = os.path.join(directory, image.filename)
    image.file.seek(0)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return image_path