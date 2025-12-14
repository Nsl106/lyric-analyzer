import json
import os
import re
from pathlib import Path

import lyricsgenius
from dotenv import load_dotenv

load_dotenv()
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")

if not GENIUS_TOKEN:
    raise RuntimeError("GENIUS_TOKEN not found in environment")

def sanitize(name: str) -> str:
    """Filesystem-safe name"""
    return re.sub(r"[^\w\- ]", "", name).strip().replace(" ", "-").lower()


def fetch_album(search_artist_name: str, search_album_name: str):
    genius = lyricsgenius.Genius(
        GENIUS_TOKEN,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
        remove_section_headers=False
    )

    album = genius.search_album(search_album_name, search_artist_name)
    if album is None:
        raise ValueError("Album not found")

    actual_artist_name = album.artist["name"]
    actual_album_name = album.name

    artist_dir = sanitize(actual_artist_name)
    album_dir = sanitize(actual_album_name)

    base_path = Path("data/lyrics") / artist_dir / album_dir
    base_path.mkdir(parents=True, exist_ok=True)

    metadata = {
        "artist": actual_artist_name,
        "album": actual_album_name,
        "tracks": []
    }

    for track in album.tracks:
        num, song = track
        if not song or not song.lyrics:
            continue

        filename = f"{num:02d}_{sanitize(song.title)}.txt"
        file_path = base_path / filename

        if file_path.exists():
            print(f"Skipping existing: {filename}")
        else:
            file_path.write_text(song.lyrics, encoding="utf-8")
            print(f"Saved: {filename}")

        metadata["tracks"].append({
            "title": song.title,
            "filename": filename
        })

    with open(base_path / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nLyrics cached at: {base_path}")


if __name__ == "__main__":
    artist = input("Artist name: ")
    album = input("Album name: ")
    fetch_album(artist, album)
