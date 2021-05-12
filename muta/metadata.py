from datetime import datetime


class SongMetadata:
    track_id: int = None
    name: str = None
    artist: str = None
    length: float = None


class AlbumMetadata:
    title: str = None
    album_artist: str = None
    release_date: datetime = None
    songs: dict[int, SongMetadata] = dict()
