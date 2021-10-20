import re
from abc import ABCMeta, abstractmethod
from datetime import datetime

from bs4 import BeautifulSoup

from muta.metadata import SongMetadata, AlbumMetadata


class Parser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, text):
        pass


class MoraParser(Parser):
    def parse(self, text):
        soup = BeautifulSoup(text, "html.parser")
        album = AlbumMetadata()

        # Album
        album.title = soup.select("div#package_title")[0].text.strip()
        album.album_artist = soup.select("div#package_artist")[0].text.strip()
        album.release_date = datetime.strptime(soup.select("div#package_release")[0].text.strip(), "%Y.%m.%d")

        # Songs
        table_body = soup.select(".package_table")[0].findNext('tbody')
        for line in table_body.select("tr"):
            song = SongMetadata()
            for cell in line.select("td"):
                if "<!--No-->" in str(cell):
                    song.track_id = int(cell.text.strip())
                elif "<!--アーティスト名-->" in str(cell):
                    song.artist = cell.text.strip()
                elif "<!--楽曲名-->" in str(cell):
                    song.name = cell.text.strip()
                elif "<!--時間-->" in str(cell):
                    time_strings = re.findall(r"<!--時間-->(.*)<!--//時間-->", str(cell))
                    if len(time_strings) == 1:
                        length_list = time_strings[0].split(":")
                        song.length = int(length_list[0]) * 60 + int(length_list[1])
            album.songs[song.track_id] = song

        return album


class AppleMusicParser(Parser):
    @staticmethod
    def get_artists_string(line):
        artists = []
        for artist_link in line.select('a'):
            artists.append(artist_link.text)
        return ";".join(artists)

    def parse(self, text):
        soup = BeautifulSoup(text, "html.parser")
        album = AlbumMetadata()

        # Album
        album.title = soup.select("h1.product-name")[0].text.strip()
        album.album_artist = self.get_artists_string(soup.select("div.product-creator")[0])
        _release_date = soup.select("p.song-released-container")[0].text.strip()
        if "年" in _release_date:
            album.release_date = datetime.strptime(_release_date, "%Y年%m月%d日")
        elif "년" in _release_date:
            album.release_date = datetime.strptime(_release_date, "%Y년 %m월 %d일")
        else:
            album.release_date = datetime.strptime(_release_date, "%B %d, %Y")

        # Songs
        table_body = soup.select("div.songs-list")[0]
        offset = 0
        for line in table_body.select("div.songs-list-row"):
            if len(line.select('div.songs-list-row__song-index')) == 0:
                continue
            song = SongMetadata()
            song.track_id = int(line.select('span.songs-list-row__column-data')[0].text.strip())
            song.name = line.select('div.songs-list-row__song-name')[0].text.strip()
            song_length_text = line.select('time.songs-list-row__length')
            if len(song_length_text) == 0:
                continue
            length_list = song_length_text[0].text.strip().split(":")

            song.length = int(length_list[0]) * 60 + int(length_list[1])

            if len(line.select('div.songs-list-row__by-line')) > 0:
                song.artist = self.get_artists_string(line.select('div.songs-list-row__by-line')[0])
            else:
                # Apple Music do not display artists if same with album artists
                song.artist = album.album_artist

            if song.track_id in album.songs:
                if song.track_id == 1:
                    offset = len(album.songs)
                album.songs[offset + song.track_id] = song
            else:
                album.songs[song.track_id] = song

        return album


class SmartParser:
    def __init__(self, url):
        if "music.apple.com" in url:
            self.parser = AppleMusicParser()
        elif "mora.jp" in url:
            self.parser = MoraParser()
        else:
            raise ValueError

    def parse(self, text):
        if self.parser:
            return self.parser.parse(text)
