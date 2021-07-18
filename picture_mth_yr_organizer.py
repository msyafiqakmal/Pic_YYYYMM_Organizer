import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import shutil
import imghdr
import yaml

with open('config.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    identified_file = yaml.load(file, Loader=yaml.FullLoader)

path = identified_file['image_folder']


# instantiate date to filter those without datetimeoriginal in image metadata
originalpicdate = datetime.strptime("1970:01:01", "%Y:%m:%d")

# Function to extract date from metadata
def getpicdate(pathx):
    image = Image.open(pathx)
    exifdata = image.getexif()
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if tag == "DateTimeOriginal" :
            originalpicdate = datetime.strptime(data, "%Y:%m:%d %H:%M:%S")
    return originalpicdate

# create folder
for filename in os.listdir(path):
    try :
        #will skip dir and non-image
        imghdr.what(path+filename) 

        picdate = getpicdate(path+filename)
        picyear = str(picdate.year)

        # zfill to make it 01 instead of 1 e.g. for january
        picmonth = str(picdate.month).zfill(2)
        newpath = path+picyear+"/"+picmonth +"/"

        #Skip if the file dont have datetime metadata
        if (picdate != datetime.strptime("1970:01:01", "%Y:%m:%d")):
            MYDIR = (newpath)
            CHECK_FOLDER = os.path.isdir(MYDIR)

            # If folder doesn't exist, then create it.
            if not CHECK_FOLDER:
                os.makedirs(MYDIR)
                print("created folder : ", MYDIR)
                shutil.move(path+filename, newpath+filename)
            else:
                shutil.move(path+filename, newpath+filename)
                
    except Exception as e:
        print("error reported for the file {}:".format(filename))
        print(e)

