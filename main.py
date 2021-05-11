from os import walk
from os import chdir

import data_source
import tagger

album_url = r"https://mora.jp/package/43000021/SQEX-10642-5/"
music_dir = r"F:\Octopath Traveler\Disc 4"

CHROME_BINARY = r"C:\Users\fang2hou\AppData\Local\Google\Chrome SxS\Application\chrome.exe"

source = data_source.Mora(chromedriver_path=CHROME_BINARY)
album_data = source.get_data_by_url(album_url)

_, _, music_files = next(walk(music_dir))
chdir(music_dir)

for music_file in music_files:
    tagger.update_file(music_file, album_data, 60)