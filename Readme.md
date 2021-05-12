# Muta

This is a tool for updating / creating tags for songs.  
这是一个用于创建或是更新音乐文件标签的工具。

You can specify the web page which contains rich information of songs and merge that into your files locally.  
你可以指定一个包含足量元数据的网页，然后将其内容固化到你的本地音乐文件中。

The basic protocol can be outlined as:  
基本原理操作如下：

1. Fetch source of web page.  
   获取网页源代码。
2. Parse the source of page to metadata.  
   解析网页，处理为元数据。
3. Modify tags.  
   修改标签。

# Support sites 支持网站

Currently, Apple Music and mora.jp are supported.  
目前支持 Apple Music 及 mora.js。

# Dependencies 依赖

```plaintext
Chrome Browser
mutagen
chromedriver-binary
```

# Sample code 样例代码

```python
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
CHROME_BINARY = r"C:\chrome.exe"

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
```