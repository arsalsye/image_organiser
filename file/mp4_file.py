import os
import ffmpeg
from file.media_file import MediaFile
from image_metadata_extractor import extract_metadata
from model.image_metadata import ImageMetadata


class Mp4File(MediaFile):

    def __init__(self, filepath):
        self.filepath = filepath
        self._metadata = self._extract_metadata()

    def get_output_destination(self, output_path: str):
        return None

    def _extract_metadata(self) -> ImageMetadata:
        probe = ffmpeg.probe(self.filepath)
        metadata = probe['format']['tags']
        creation_time = metadata.get('creation_time', 'Unknown')

        return None


'''


def get_metadata(file_path):
    
    return creation_time

file_path = 'path_to_your_video.mp4'
print(get_metadata(file_path))

'''