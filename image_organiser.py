import glob
import os.path
import shutil
from pathlib import Path

from tqdm import tqdm

from app import logger
from file.media_file import MediaFile
from file.media_file_factory import MediaFileFactory


class ImageOrganiser:

    def __init__(self, dry_run):
        self.dry_run: bool = dry_run
        self.ignored_filed_extensions = ["ini", "mht", "m4v"]

    def file_extension_allowed(self, file):
        return file.split(".")[-1] not in self.ignored_filed_extensions

    def run(self, input_dir: str, output_dir: str):
        files = [file for file in glob.glob(input_dir, recursive=True) if self.file_extension_allowed(file)]
        media_file_factory = MediaFileFactory()

        logger.info(f"Found {len(files)} files")

        with tqdm(total=len(files)) as progress_bar:
            for file in files:
                media_file = media_file_factory.create_file(file)

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
