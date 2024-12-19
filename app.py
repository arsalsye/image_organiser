import logging

from image_organiser import ImageOrganiser

logger = logging.getLogger(__name__)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    input_dir = "C:\\Users\\arsal\\Pictures\\photos_to_sort\\*"
    output_dir = "C:\\Users\\arsal\\Pictures\\sorted_photos"

    ImageOrganiser(dry_run=True).run(input_dir, output_dir)
