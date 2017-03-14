import datetime
import os

#Ext Deps
import exifread

def _get_if_exist(data, key):
    if key in data:
        return data[key]
    return None

def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

def _get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None

    gps_latitude = _get_if_exist(exif_data, 'GPS GPSLatitude')
    gps_latitude_ref = _get_if_exist(exif_data, 'GPS GPSLatitudeRef')
    gps_longitude = _get_if_exist(exif_data, 'GPS GPSLongitude')
    gps_longitude_ref = _get_if_exist(exif_data, 'GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = _convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon
    return lat, lon

def _getImageDetail(img):
    img=open(img)
    exif=exifread.process_file(img,details=False)
    (lat,lon)=_get_exif_location(exif)
    img.close()
    return {'name':img.name,
            'lat':lat,
            'lon':lon,
            'dt':datetime.datetime.strptime(str(exif['Image DateTime']),'%Y:%m:%d %H:%M:%S')
        }

def _serializeTime(obj):
    if isinstance(obj,datetime.datetime):
        serial=obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def details(imgpath):
    if os.path.isdir(imgpath):
        imgFiles=[f for f in os.listdir(imgpath) if os.path.isfile(os.path.join(imgpath,f))]
        images=[]
        for f in imgFiles:
            images.append(_getImageDetail(os.path.join(imgpath,f)))
        return images
    else:
        return [_getImageDetail(imgpath)]

def storeDetails(data,fname='imgData.json'):
    import json
    with open(fname,'w') as fp:
        json.dump(data,fp,default=_serializeTime,indent=4)
        fp.close()

def _timeHook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            pass
    return json_dict

def getDetails(fname='imgData.json'):
    import json
    with open(fname,'r') as fp:
        data=json.load(fp,object_hook=_timeHook)
        fp.close()
        return data

if __name__=="__main__":
    import pprint
    a=details('gopropics')
    pprint.PrettyPrinter(indent=4).pprint(a)
