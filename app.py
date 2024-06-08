import calendar
import glob
import os.path
import shutil
from concurrent.futures import ThreadPoolExecutor

import pillow_heif

from image_metadata_extractor import extract_metadata
from model.image_metadata import ImageMetadata
from tqdm import tqdm

def get_output_path(base_output_path, image_metadata: ImageMetadata) -> str:
    if image_metadata.created_on is None:
        return os.path.join(base_output_path, f"Misc")

    year = image_metadata.created_on.year
    month = image_metadata.created_on.month
    month_str = calendar.month_name[month]

    if image_metadata.address.city is not None:
        location = f" - {image_metadata.address.city}"
    elif image_metadata.address.country is not None:
        location = f" - {image_metadata.address.country}"
    else:
        location = ""

    relative_path = f"{year}\\{month_str}{location}"
    return os.path.join(base_output_path, relative_path)


def is_jpeg(image_path):
    return ".jpg" in image_path or ".jpeg" in image_path or ".JPG" in image_path

from pathlib import Path


def move_file(image_path, output_dir, dry_run, progress_bar):
    image_metadata = extract_metadata(image_path)
    output_path = get_output_path(output_dir, image_metadata)

    if dry_run:
        print(f"(Dry Run) - Would move {image_metadata.file_path} to {output_path}\n")
    else:
        os.makedirs(output_path, exist_ok=True)

        my_file = Path(f"{output_path}\\{os.path.basename(image_metadata.file_path)}")
        if my_file.exists():
            os.remove(f"{output_path}\\{os.path.basename(image_metadata.file_path)}")
        shutil.move(image_metadata.file_path, output_path)
        print(f"Moved {image_metadata.file_path} to {output_path}")
        progress_bar.update(1)


def is_file_format_supported(file_path):
    return is_jpeg(file_path) or ".HEIC" in file_path


def run(input_dir, output_dir, dry_run):
    files = glob.glob(input_dir, recursive=True)

    pillow_heif.register_heif_opener()

    supported_files = [file for file in files if is_file_format_supported(file)]
    print(f"Found {len(supported_files)} images to move")

    with tqdm(total=len(supported_files)) as progress_bar:
        with ThreadPoolExecutor(max_workers=8) as executor:
            for image_path in supported_files:
                executor.submit(move_file, image_path, output_dir, dry_run, progress_bar)


'''
Given an input folder with some images:
    - Group them into folders by
      - Location
      - Year-month
    For example) 2024/June - Santorini

Deal with cases where a trip spans several months (for ex last day of May and first day of June)
Have a progress bar to know how long it will take
Deal with cases where we don't have any metadata

How to deal with photos of other formats? HEIC?
'''
if __name__ == "__main__":
    input_dir = "C:\\Users\\arsal\\Documents\\photos_to_sort\\*"
    output_dir = "C:\\Users\\arsal\\Picutres\\sorted_photos"
    dry_run = False
    run(input_dir, output_dir, dry_run)
