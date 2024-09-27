import os

from file.media_file import MediaFile
from image_metadata_extractor import extract_metadata
from model.image_metadata import ImageMetadata


class HeicFile(MediaFile):

    def __init__(self, filepath):
        self.filepath = filepath
        self._metadata = self._extract_metadata()

    def get_output_destination(self, output_path: str):
        if self._metadata.created_on is None:
            return os.path.join(output_path, "Misc")

        year = self._metadata.created_on.year

        if self._metadata.address.country is not None:
            location = f"{self._metadata.address.country}"
        else:
            location = ""

        relative_path = f"{year}\\{location}"
        return os.path.join(output_path, relative_path)

    def _extract_metadata(self) -> ImageMetadata:
        return extract_metadata(self.filepath)
