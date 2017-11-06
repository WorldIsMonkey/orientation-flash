from PIL import Image
from os import listdir
from os.path import isfile, join, basename

path = "./pics/"

files = listdir(path)
i = 0
for directory in files:
    subpath = join(path, directory)
    if not isfile(subpath):
        i += 1
        with open(join('.','data','pic2','%s.config'%i), 'wb') as config_file:
            config_file.write(('%s\nN/A\nN/A\nN/A\nN/A\nN/A\n'%directory).encode('utf-8'))
        for pic_quality in [['orig.jpg', '4'], ['L1.jpg', '3'], ['L2.jpg', '2'], ['L3.jpg', '1']]:
            im=Image.open(join(subpath, pic_quality[0]))
            size = 1280, 720
            im_resized = im.resize(size, Image.ANTIALIAS)
            im_resized.save(join('.', 'data', 'pic2', "media", "%s-%s.jpg"%(i, pic_quality[1])), "JPEG")
        