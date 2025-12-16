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

def sanitize_filename(name: str) -> str:
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

    artist_dir = sanitize_filename(actual_artist_name)
    album_dir = sanitize_filename(actual_album_name)

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

        filename = f"{num:02d}_{sanitize_filename(song.title)}.txt"
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


def fetch_song(search_artist_name: str, search_song_title: str):
    genius = lyricsgenius.Genius(
        GENIUS_TOKEN,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
        remove_section_headers=False,
        timeout=15,
        retries=2,
    )

    song = genius.search_song(search_song_title, search_artist_name, )
    if song is None or not song.lyrics:
        raise ValueError("Song not found or has no lyrics")

    actual_artist_name = song.artist
    actual_song_title = song.title

    artist_dir = sanitize_filename(actual_artist_name)
    song_dir = sanitize_filename(actual_song_title)

    base_path = Path("data/lyrics") / artist_dir / "_singles"
    base_path.mkdir(parents=True, exist_ok=True)

    lyrics_filename = f"{song_dir}.txt"
    lyrics_path = base_path / lyrics_filename

    if lyrics_path.exists():
        print(f"Skipping existing: {lyrics_filename}")
    else:
        lyrics_path.write_text(song.lyrics, encoding="utf-8")
        # print(f"Saved: {lyrics_filename}")

    return {
        "missing": False,
        "actual_artist": actual_artist_name,
        "actual_title": actual_song_title,
        "lyrics_path": str(Path(artist_dir) / "_singles" / lyrics_filename),
    }
