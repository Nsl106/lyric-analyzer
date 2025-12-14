import json
from pathlib import Path
from typing import Any


def load_album(artist: str, album: str) -> tuple[list[str], dict]:
    artist = artist.replace(" ", "_")
    album = album.replace(" ", "_")

    base_path = Path("data/lyrics") / artist / album

    if not base_path.exists():
        raise FileNotFoundError("Album not cached yet")

    metadata = load_metadata(artist, album)

    text = []

    for track in metadata["tracks"]:
        file_path = base_path / track["filename"]
        text.append(file_path.read_text(encoding="utf-8"))


    return text, metadata

def load_metadata(artist: str, album: str) -> dict:
    artist = artist.replace(" ", "_")
    album = album.replace(" ", "_")

    metadata_path = (
            Path("data/lyrics") / artist / album / "metadata.json"
    )

    if not metadata_path.exists():
        raise FileNotFoundError("metadata.json not found for album")

    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)