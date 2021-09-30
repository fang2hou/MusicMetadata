from muta.driver import Driver
from muta.parser import SmartParser
from muta.tagger import MatchingMethod
from muta.tagger import Tagger

# Configs
ALBUM_MAIN = r"https://music.apple.com/us/album/"
ALBUM_URL = r"the-essential-michael-jackson/159292399"
# ALBUM_MAIN = r"https://mora.jp/package/"
# ALBUM_URL = r"43000006/00600406610478/"
MUSIC_DIR = r"F:\Michael Jackson\The Essential Michael Jackson\Disc 2"
MATCHING = MatchingMethod.Track
RENAME = True
START_AT = 22
OFFSET = 0
CHROME_BINARY = r"C:\Developer\Chrome\App\chrome.exe"

ALBUM_URL = ALBUM_MAIN + ALBUM_URL
# Core
driver = Driver(chromedriver_path=CHROME_BINARY)
page = driver.fetch(url=ALBUM_URL)
driver.quit()

assert len(page) > 0

parser = SmartParser(ALBUM_URL)
album_metadata = parser.parse(text=page)

for m in album_metadata.songs.items():
    # if m[0] > 32:
    #     _a = m[0] - 32
    # elif m[0] > 16:
    #     _a = m[0] - 16
    # else:
    #     _a = m[0]
    _a = m[0]
    print("{:02d}. {}".format(_a, m[1].name))

assert len(album_metadata.songs) > 0

tagger = Tagger(MATCHING, RENAME, START_AT, OFFSET)
tagger.tag_in_directory(MUSIC_DIR, album_metadata)
