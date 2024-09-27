import pillow_heif

from file.heic_file import HeicFile
from file.jpeg_file import JpegFile
from file.media_file import MediaFile
from file.png_file import PngFile


class MediaFileFactory:

    def __init__(self):
        pillow_heif.register_heif_opener()

    def create_file(self, filepath) -> MediaFile:
        if self._is_jpeg(filepath):
            return JpegFile(filepath)
        elif self._is_png(filepath):
            return PngFile(filepath)
        elif self._is_heic(filepath):
            return HeicFile(filepath)
        else:
            raise ValueError(f"Unsupported file type: {filepath}")

    @staticmethod
    def _is_jpeg(image_path):
        image_path_lower = image_path.lower()
        return ".jpg" in image_path_lower or ".jpeg" in image_path_lower

    @staticmethod
    def _is_png(image_path):
        image_path_lower = image_path.lower()
        return ".png" in image_path_lower

    @staticmethod
    def _is_heic(image_path):
        image_path_lower = image_path.lower()
        return ".heic" in image_path_lower