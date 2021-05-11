import os
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

from datetime import datetime

def update_file(file_path, database, start=None):
    release = datetime.strptime(database['release_date'], "%Y.%m.%d")

    if not start:
        start = 1

    if file_path[-4:] == '.m4a':
        audio = MP4(file_path)
        track = audio.tags['trkn'][0][0]
        db_id = str(track + start - 1)
        audio[u'\xa9nam'] = [database['songs'][db_id]['name']]
        audio[u'\xa9alb'] = [database['album']]
        audio[u'\xa9ART'] = database['songs'][db_id]['artist'].split(";")
        audio.save()

    elif file_path[-5:] == '.flac':
        audio = FLAC(file_path)
        if 'tracknumber' in audio.tags:
            track = int(audio['tracknumber'][0])
        else:
            track = int(file_path[0:2])
            audio['tracknumber'] = [str(track)]


        db_id = str(track + start - 1)

        audio['title'] = [database['songs'][db_id]['name']]
        audio['album'] = [database['album']]
        database['songs'][db_id]['artist'] = database['songs'][db_id]['artist'].replace("祖堅 正慶", "祖堅正慶")
        audio['artist'] = [database['songs'][db_id]['artist']]
        audio['date'] = [str(release.year)]
        audio.save()

        new_name = "{:02d} {}.flac".format(track, database['songs'][db_id]['name'])
        new_name = new_name.replace(": ", "：")
        os.rename(file_path, new_name)