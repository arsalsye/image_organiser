import glob
import logging
import os.path
import shutil
from pathlib import Path

import pillow_heif
from tqdm import tqdm

from file.media_file import MediaFile
from file.media_file_factory import MediaFileFactory

logger = logging.getLogger(__name__)


class ImageOrganiser:

    def __init__(self, dry_run):
        self.dry_run: bool = dry_run

    def run(self, input_dir: str, output_dir: str):
        files = glob.glob(input_dir, recursive=True)
        media_file_factory = MediaFileFactory()
        media_files = [media_file_factory.create_file(file) for file in files]

        logger.info(f"Found {len(media_files)} images to move")

        if len(media_files) == 0:
            logger.warn(f"No files to move, exiting..")
            return

        with tqdm(total=len(media_files)) as progress_bar:
            for media_file in media_files:
                try:
                    self.move_file(media_file, output_dir)
                except Exception as e:
                    logger.exception(e)
                progress_bar.update(1)

    def move_file(self, media_file: MediaFile, output_dir):
        output_path = media_file.get_output_destination(output_dir)

        if self.dry_run:
            logger.info(f"(Dry Run) - Would move {media_file.filepath} to {output_path}")
        else:
            os.makedirs(output_path, exist_ok=True)

            my_file = Path(f"{output_path}\\{os.path.basename(media_file.filepath)}")
            if my_file.exists():
                logger.warn(f"File at path {my_file} already exists")
                os.rename(f"{output_path}\\{os.path.basename(media_file.filepath)}",
                          f"{output_path}\\Copy_{os.path.basename(media_file.filepath)}")
            shutil.move(media_file.filepath, output_path)

            logger.info(f"Moved {media_file.filepath} to {output_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    input_dir = "C:\\Users\\arsal\\Documents\\test\\*"
    output_dir = "C:\\Users\\arsal\\Pictures\\sorted_photos"

    ImageOrganiser(dry_run=True).run(input_dir, output_dir)
