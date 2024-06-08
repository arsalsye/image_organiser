from datetime import datetime

import piexif
from PIL import Image
from geopy.geocoders import Nominatim

from model.address import Address
from model.image_metadata import ImageMetadata

date_format = '%Y:%m:%d %H:%M:%S'


def get_exif_data(image_path):
    image = Image.open(image_path)

    exif_data = {}

    exif_dict = piexif.load(image.info["exif"])
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[ifd]:
            exif_data[piexif.TAGS[ifd][tag]["name"]] = exif_dict[ifd][tag]

    return exif_data


def convert_to_degrees(value):
    d = float(value[0][0] / value[0][1])
    m = float(value[1][0] / value[1][1])
    s = float(value[2][0] / value[2][1])
    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(gps_data):
    if not gps_data:
        return None, None

    lat = gps_data.get('GPSLatitude')
    lat_ref = gps_data.get('GPSLatitudeRef').decode("UTF-8")
    lon = gps_data.get('GPSLongitude')
    lon_ref = gps_data.get('GPSLongitudeRef').decode("UTF-8")

    if not lat or not lon or not lat_ref or not lon_ref:
        return None, None

    latitude = convert_to_degrees(lat)
    if lat_ref != "N":
        latitude = -latitude

    longitude = convert_to_degrees(lon)
    if lon_ref != "E":
        longitude = -longitude

    return latitude, longitude


def get_location(latitude, longitude):
    if latitude is None or longitude is None:
        return None

    geoLoc = Nominatim(user_agent="GetLocation")
    return geoLoc.reverse(f"{latitude}, {longitude}", language="en-GB")


def get_created_on(exif_data):
    creation_date = exif_data.get('DateTimeOriginal') or exif_data.get('DateTime')
    if creation_date is None:
        return None
    return datetime.strptime(creation_date.decode("UTF-8"), date_format)


def get_country(location):
    if location is None:
        return None

    if "address" in location.raw.keys() and "country" in location.raw["address"].keys():
        return location.raw["address"]["country"]
    else:
        return None


def get_city(location):
    if location is None:
        return None

    if "address" in location.raw.keys() and "city" in location.raw["address"].keys():
        return location.raw["address"]["city"]
    else:
        return None


def extract_metadata(image_path: str) -> ImageMetadata:
    #print(f"Extracting metadata for {image_path}")
    exif_data = get_exif_data(image_path)
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
