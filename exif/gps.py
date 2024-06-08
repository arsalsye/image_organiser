from geopy.geocoders import Nominatim


def convert_to_degrees(value):
    d = float(value[0][0] / value[0][1])
    m = float(value[1][0] / value[1][1])
    s = float(value[2][0] / value[2][1])
    return d + (m / 60.0) + (s / 3600.0)



def get_lat_lon(exif_data):
    if not exif_data:
        return None, None

    lat = exif_data.get('GPSLatitude')
    lat_ref = exif_data.get('GPSLatitudeRef')
    lon = exif_data.get('GPSLongitude')
    lon_ref = exif_data.get('GPSLongitudeRef')

    if not lat or not lon or not lat_ref or not lon_ref:
        return None, None

    latitude = convert_to_degrees(lat)
    if lat_ref.decode("UTF-8") != "N":
        latitude = -latitude

    longitude = convert_to_degrees(lon)
    if lon_ref.decode("UTF-8") != "E":
        longitude = -longitude

    return latitude, longitude


def get_location(latitude, longitude):
    if latitude is None or longitude is None:
        return None

    geoLoc = Nominatim(user_agent="GetLocation")
    return geoLoc.reverse(f"{latitude}, {longitude}", language="en-GB")

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
