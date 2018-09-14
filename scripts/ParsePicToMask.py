from PIL import Image
from os import listdir
from os.path import isfile, join, basename

path = "./pics/"

files = listdir(path)
i = 0
for filename in files:
    filepath = join(path, filename)
    if (isfile(filepath) and ".jpg" in filename):
        i += 1
        im = Image.open(filepath)
        size = 1280, 720
        im_resized = im.resize(size, Image.ANTIALIAS)
        # new_filepath = join(path, "newpics", filename)
        # im_resized.save(new_filepath, "JPEG")
        new_path = join('..', 'data', 'pic1')
        answer = basename(filename).split('.')[0]
        config_string = "%s\nN/A\nN/A\nN/A\nN/A\nN/A\n" % answer
        with open(join(new_path, "%s.config" % i), 'wb') as file:
            file.write(config_string.encode('utf-8'))
        im_resized.save(join(new_path, "media", "%s-1.jpg"%i), "JPEG")
        im_resized.save(join(new_path, "media", "%s-2.jpg"%i), "JPEG")
