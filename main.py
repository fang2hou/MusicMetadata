from os import walk
from os import chdir

import data_source
import tagger

# album_url = r"https://mora.jp/package/43000021/SQEX-10203/"
# music_dir = r"F:\FFXIV\FINAL FANTASY XIV Field Tracks"
#
# CHROME_BINARY = r"C:\Users\fang2hou\AppData\Local\Google\Chrome SxS\Application\chrome.exe"
#
# source = data_source.Mora(chromedriver_path=CHROME_BINARY)
# album_data = source.get_data_by_url(album_url)
#
# _, _, music_files = next(walk(music_dir))
# chdir(music_dir)

# for music_file in music_files:
#     tagger.update_file(music_file, album_data, 1)

album_url = r"https://music.apple.com/cn/album/%E5%8E%9F%E7%A5%9E-%E6%BC%A9%E6%B6%A1-%E8%90%BD%E6%98%9F%E4%B8%8E%E5%86%B0%E5%B1%B1-%E6%B8%B8%E6%88%8F-%E5%8E%9F%E7%A5%9E-%E5%8E%9F%E5%A3%B0%E9%9F%B3%E4%B9%90/1559217220"
music_dir = r"F:\Genshin\原神-漩涡、落星与冰山 (游戏《原神》原声音乐)"

CHROME_BINARY = r"C:\Users\fang2hou\AppData\Local\Google\Chrome SxS\Application\chrome.exe"

source = data_source.AppleMusic(chromedriver_path=CHROME_BINARY)
album_data = source.get_data_by_url(album_url)
print(album_data)

_, _, music_files = next(walk(music_dir))
chdir(music_dir)

for music_file in music_files:
    tagger.update_file(music_file, album_data, 1)