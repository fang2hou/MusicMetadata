from muta.driver import Driver
from muta.parser import SmartParser
from muta.tagger import MatchingMethod
from muta.tagger import Tagger

# Configs
ALBUM_URL = r"https://music.apple.com/cn/album/七里香/536114662"
MUSIC_DIR = r"F:\周杰伦\七里香"
MATCHING = MatchingMethod.Name
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
