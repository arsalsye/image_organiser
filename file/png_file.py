import os

from file.media_file import MediaFile
from image_metadata_extractor import extract_metadata
from model.image_metadata import ImageMetadata


class PngFile(MediaFile):

    def __init__(self, filepath):
        self.filepath = filepath
        self._metadata = self._extract_metadata()

    def get_output_destination(self, output_path: str):
        return os.path.join(output_path, "Screenshots")

    def _extract_metadata(self) -> ImageMetadata:
        return extract_metadata(self.filepath)
