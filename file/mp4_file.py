import datetime
import os

from file.media_file import MediaFile
from model.image_metadata import ImageMetadata


class Mp4File(MediaFile):

    def __init__(self, filepath):
        self.filepath = filepath
        self._metadata = self._extract_metadata()

    def get_output_destination(self, output_path: str):
        if self._metadata.created_on is None:
            return os.path.join(output_path, "Misc")

        year = self._metadata.created_on.year

        return os.path.join(output_path, f"Videos\\{year}")

    def _extract_metadata(self) -> ImageMetadata:
        created_timestamp = os.path.getmtime(self.filepath)

        return ImageMetadata(
            image_path=self.filepath,
            address=None,
            created_on=datetime.datetime.fromtimestamp(created_timestamp)
        )
