from muta.driver import Driver
from muta.parser import SmartParser
from muta.tagger import Tagger
from muta.tagger import MatchingMethod

# Configs
CHROME_BINARY = r"C:\Users\fang2hou\AppData\Local\Google\Chrome SxS\Application\chrome.exe"
ALBUM_URL = r"https://music.apple.com/cn/album/%E5%8E%9F%E7%A5%9E-%E9%97%AA%E8%80%80%E7%9A%84%E7%BE%A4%E6%98%9F-%E6%B8%B8%E6%88%8F-%E5%8E%9F%E7%A5%9E-%E5%8E%9F%E5%A3%B0%E9%9F%B3%E4%B9%90/1550254705"
MUSIC_DIR = r"F:\原神-闪耀的群星 (游戏《原神》原声音乐)"
RENAME = True

# Core
driver = Driver(chromedriver_path=CHROME_BINARY)
page = driver.fetch(url=ALBUM_URL)
driver.quit()

assert len(page) > 0

parser = SmartParser(ALBUM_URL)
album_metadata = parser.parse(text=page)

assert len(album_metadata.songs) > 0

tagger = Tagger(MatchingMethod.Track, True, 1)
tagger.tag_in_directory(MUSIC_DIR, album_metadata)
