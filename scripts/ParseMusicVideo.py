import os

with open('Music.csv', 'r', encoding='utf-8') as csv:
    lines = csv.readlines()
i=0
startimes=[]
for line in lines:
    i+=1
    line_splitted = line.split(',')
    bangumi_name = line_splitted[0]
    song_name = line_splitted[1]
    singer = line_splitted[2]
    song_type = line_splitted[3]
    song_url = line_splitted[4]
    start_time = line_splitted[5].strip()
    startimes.append(start_time)
    with open(os.path.join('data','music','%s.config'%i), 'wb') as config_file:
        if 'op' in song_type.lower():
            song_type_numeral='2'
        elif 'ed' in song_type.lower():
            song_type_numeral='3'
        elif '插入曲' in song_type:
            song_type_numeral='4'
        else:
            song_type_numeral='1'
        conf_string = '%s\n%s\nN/A\nN/A\nN/A\nN/A\n%s\n'%(bangumi_name, song_name, song_type_numeral)
        config_file.write(conf_string.encode('utf-8'))
    if not os.path.isdir("download"):
        os.makedirs('download')
    os.system("youtube-dl -o 'download/%s' %s"%(i, song_url))
for filename in os.listdir('download'):
    full_filename = os.path.join('download', filename)
    index = filename.split('.')[0]
    if index:
        index=int(index)
        os.system("ffmpeg -ss %s -t 0:30 -i %s -s 1920x720 %s"%(startimes[index-1], full_filename, os.path.join('data', 'music', 'media', str(index)+'.mp4')))
        os.system("ffmpeg -ss %s -t 0:20 -i %s %s"%(startimes[index-1], full_filename, os.path.join('data', 'music', 'media', str(index)+'.mp3')))