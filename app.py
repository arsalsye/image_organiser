import glob
import os.path
import shutil
from pathlib import Path
import logging
import pillow_heif
from tqdm import tqdm

from image_metadata_extractor import extract_metadata
from model.image_metadata import ImageMetadata

logger = logging.getLogger(__name__)

def get_output_path(base_output_path, image_metadata: ImageMetadata) -> str:
    if ".png" in image_metadata.file_path:
        return os.path.join(base_output_path, "Screenshots")

    if image_metadata.created_on is None:
        return os.path.join(base_output_path, "Misc")

    year = image_metadata.created_on.year

    if image_metadata.address.country is not None:
        location = f"{image_metadata.address.country}"
    else:
        location = ""

    relative_path = f"{year}\\{location}"
    return os.path.join(base_output_path, relative_path)


def is_jpeg(image_path):
    return ".jpg" in image_path or ".jpeg" in image_path or ".JPG" in image_path or ".JPEG" in image_path


def move_file(image_path, output_dir, dry_run):
    image_metadata = extract_metadata(image_path)
    output_path = get_output_path(output_dir, image_metadata)

    if dry_run:
        logger.info(f"(Dry Run) - Would move {image_metadata.file_path} to {output_path}")
    else:
        os.makedirs(output_path, exist_ok=True)

        my_file = Path(f"{output_path}\\{os.path.basename(image_metadata.file_path)}")
        if my_file.exists():
            logger.warn(f"File at path {my_file} already exists")
            os.rename(f"{output_path}\\{os.path.basename(image_metadata.file_path)}", f"{output_path}\\Copy_{os.path.basename(image_metadata.file_path)}")
        shutil.move(image_metadata.file_path, output_path)

        logger.info(f"Moved {image_metadata.file_path} to {output_path}")


def is_file_format_supported(file_path):
    return is_jpeg(file_path) or ".HEIC" in file_path or ".png" in file_path


def run(input_dir, output_dir, dry_run):
    files = glob.glob(input_dir, recursive=True)

    pillow_heif.register_heif_opener()

    supported_files = [file for file in files if is_file_format_supported(file)]
    logger.info(f"Found {len(supported_files)} images to move")

    if len(supported_files) == 0:
        return

    with tqdm(total=len(supported_files)) as progress_bar:
        for image_path in supported_files:
            try:
                move_file(image_path, output_dir, dry_run)
            except Exception as e:
                logger.exception(e)
            progress_bar.update(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    input_dir = "C:\\Users\\arsal\\Documents\\photos_to_sort\\*"
    output_dir = "C:\\Users\\arsal\\Pictures\\sorted_photos"
    dry_run = False
    run(input_dir, output_dir, dry_run)
