from enum import Enum
from os import walk, chdir, rename

from mutagen.flac import FLAC
from mutagen.mp4 import MP4

from muta.metadata import AlbumMetadata


class MatchingMethod(Enum):
    Track = 1
    TrackInName = 2
    Name = 3
    Length = 4


def force_trans(string):
    string = string.replace("祖堅 正慶", "祖堅正慶")
    return string


class Tagger:
    def __init__(self, matching_method: MatchingMethod, auto_rename=False, start=1):
        self.matching_method = matching_method
        self.rename = auto_rename
        self.start = start

    @staticmethod
    def __guess_track_id_by_length(song_length: float, metadata: AlbumMetadata) -> int:
        temp_min_abs_second = abs(metadata.songs[1].length - song_length)
        temp_id = 1
        for song_id in metadata.songs:
            temp_abs_second = abs(metadata.songs[song_id].length - song_length)
            if temp_abs_second < temp_min_abs_second:
                temp_min_abs_second = temp_abs_second
                temp_id = song_id
        return temp_id

    def tag_mp4_file(self, file_path: str, metadata: AlbumMetadata):
        if file_path[-4:] != '.m4a':
            raise TypeError

        audio = MP4(file_path)

        # Matching
        if self.matching_method == MatchingMethod.Track:
            if 'trkn' not in audio.tags:
                raise ValueError
            else:
                track = int(audio.tags['trkn'][0][0])
        elif self.matching_method == MatchingMethod.TrackInName:
            track = int(file_path[0:2])
        elif self.matching_method == MatchingMethod.Name:
            file_name = file_path.split(" ")[-1].strip('.m4a')
            track = 0
            for song_id in metadata.songs:
                if file_name == metadata.songs[song_id].name:
                    track = song_id
                    audio.tags['trkn'] = [(str(song_id) , str(len(metadata.songs)))]
                    break
            if track == 0:
                raise ValueError
        else:
            track = self.__guess_track_id_by_length(audio.info['length'], metadata)

        # Write metadata to audio file
        metadata_song_id = track + self.start - 1
        audio[u'\xa9nam'] = [metadata.songs[metadata_song_id].name]  # Song Title
        audio[u'\xa9ART'] = [force_trans(metadata.songs[metadata_song_id].artist)]  # Song Artist
        audio[u'\xa9alb'] = [metadata.title]  # Album Title
        audio['aART'] = [metadata.album_artist]  # Album Artist
        audio[u'\xa9day'] = [str(metadata.release_date.year)]  # Album Year
        audio.save()

        # rename
        if self.rename:
            new_name = "{:02d} {}.m4a".format(track, metadata.songs[metadata_song_id].name)
            new_name = new_name.replace(": ", "：")
            new_name = new_name.replace(" / ", "／")
            rename(file_path, new_name)

    def tag_flac_file(self, file_path: str, metadata: AlbumMetadata):
        if file_path[-5:] != '.flac':
            raise TypeError

        audio = FLAC(file_path)

        # Matching
        if self.matching_method == MatchingMethod.Track:
            if 'tracknumber' not in audio.tags:
                raise ValueError
            else:
                track = int(audio['tracknumber'][0])
        elif self.matching_method == MatchingMethod.TrackInName:
            track = int(file_path[0:2]) - self.start + 1
            audio['tracknumber'] = [str(track)]
        elif self.matching_method == MatchingMethod.Name:
            file_names = file_path.split(" ")

            if len(file_names) > 1:
                file_name = file_names[1]
            else:
                file_name = file_names[0]

            file_name = file_name.split("-")[-1].strip('.flac').strip()
            track = 0
            for song_id in metadata.songs:
                if file_name in metadata.songs[song_id].name:
                    track = song_id - self.start + 1
                    audio['tracknumber'] = [str(track)]
                    break
            if track == 0:
                raise ValueError
        else:
            track = self.__guess_track_id_by_length(audio.info['length'], metadata)

        # Write metadata to audio file
        metadata_song_id = track + self.start - 1
        audio['title'] = [metadata.songs[metadata_song_id].name]  # Song Title
        audio['artist'] = [force_trans(metadata.songs[metadata_song_id].artist)]  # Song Artist
        audio['album'] = [metadata.title]  # Album Title
        audio['albumartist'] = [metadata.album_artist]  # Album Artist
        audio['date'] = [str(metadata.release_date.year)]  # Album Year
        audio.save()

        # rename
        if self.rename:
            new_name = "{:02d} {}.flac".format(track, metadata.songs[metadata_song_id].name)
            new_name = new_name.replace(": ", "：")
            new_name = new_name.replace(" / ", "／")
            new_name = new_name.replace("/ ", "／")
            rename(file_path, new_name)

    def tag_file(self, file_path: str, metadata: AlbumMetadata):
        if file_path[-4:] == '.m4a':
            self.tag_mp4_file(file_path, metadata)
        elif file_path[-5:] == '.flac':
            self.tag_flac_file(file_path, metadata)

    def tag_in_directory(self, directory_path: str, metadata: AlbumMetadata):
        chdir(directory_path)
        _, _, music_files = next(walk(directory_path))
        for music_file in music_files:
            self.tag_file(music_file, metadata)