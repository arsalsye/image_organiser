from datetime import datetime

import piexif
from PIL import Image

from exif.date import get_created_on
from exif.gps import get_lat_lon, get_location, get_country, get_city
from model.address import Address
from model.image_metadata import ImageMetadata


def extract_metadata(image_path: str) -> ImageMetadata:

    exif_data = get_exif_data(image_path)
    if exif_data is None:
        return ImageMetadata(
        image_path=image_path,
        address=None,
        created_on=None
    )

    lat, lon = get_lat_lon(exif_data)
    location = get_location(lat, lon)

    created_on = get_created_on(exif_data)

    return ImageMetadata(
        image_path=image_path,
        address=Address(
            country=get_country(location),
            city=get_city(location)
        ),
        created_on=created_on
    )


def get_exif_data(image_path):
    image = Image.open(image_path)

    exif_data = {}

    if "exif" not in image.info:
        return None

    exif_dict = piexif.load(image.info["exif"])
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[ifd]:
            exif_data[piexif.TAGS[ifd][tag]["name"]] = exif_dict[ifd][tag]

    return exif_data
