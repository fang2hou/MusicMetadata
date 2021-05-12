from muta.driver import Driver
from muta.parser import SmartParser
from muta.tagger import MatchingMethod
from muta.tagger import Tagger

# Configs
ALBUM_URL = r"https://music.apple.com/cn/album/%E5%8E%9F%E7%A5%9E-%E9%A3%8E%E4%B8%8E%E5%BC%82%E4%B9%A1%E4%BA%BA-%E6%B8%B8%E6%88%8F%E5%8E%9F%E5%A3%B0%E9%9F%B3%E4%B9%90/1519189626"
MUSIC_DIR = r"F:\原神\[200619] 原神-风与异乡人 Le Vent et les Enfants des étoiles FLAC"
MATCHING = MatchingMethod.Track
RENAME = True
START_AT = 1
CHROME_BINARY = r"C:\Users\fang2hou\AppData\Local\Google\Chrome SxS\Application\chrome.exe"

# Core
driver = Driver(chromedriver_path=CHROME_BINARY)
page = driver.fetch(url=ALBUM_URL)
driver.quit()

assert len(page) > 0

parser = SmartParser(ALBUM_URL)
album_metadata = parser.parse(text=page)

assert len(album_metadata.songs) > 0

tagger = Tagger(MATCHING, RENAME, START_AT)
tagger.tag_in_directory(MUSIC_DIR, album_metadata)
