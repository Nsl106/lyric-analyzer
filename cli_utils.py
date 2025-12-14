from pathlib import Path
from prompt_toolkit.completion import Completer, Completion

LYRICS_PATH = Path("data/lyrics")


class ArtistCompleter(Completer):
    def get_completions(self, document, complete_event):
        if not LYRICS_PATH.exists():
            return

        word = document.text.lower()

        for artist in LYRICS_PATH.iterdir():
            if artist.is_dir() and artist.name.lower().startswith(word):
                yield Completion(
                    artist.name,
                    start_position=-len(document.text)
                )


class AlbumCompleter(Completer):
    def __init__(self, artist_name: str):
        self.artist_name = artist_name.replace(" ", "_")

    def get_completions(self, document, complete_event):
        artist_path = LYRICS_PATH / self.artist_name
        if not artist_path.exists():
            return

        word = document.text.lower()

        for album in artist_path.iterdir():
            if album.is_dir() and album.name.lower().startswith(word):
                yield Completion(
                    album.name,
                    start_position=-len(document.text)
                )
