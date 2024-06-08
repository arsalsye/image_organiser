from datetime import datetime

date_format = '%Y:%m:%d %H:%M:%S'


def get_created_on(exif_data):
    creation_date = exif_data.get('DateTimeOriginal') or exif_data.get('DateTime')
    if creation_date is None:
        return None
    return datetime.strptime(creation_date.decode("UTF-8"), date_format)
