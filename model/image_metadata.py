from model.address import Address
from datetime import datetime


class ImageMetadata:

    def __init__(self, image_path: str, address: Address, created_on: datetime):
        self.file_path = image_path
        self.address = address
        self.created_on = created_on
