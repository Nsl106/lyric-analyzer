import json
from pathlib import Path


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

def load_song(artist: str, song: str) -> str:
    base_path = Path("data/lyrics") / artist / "_singles"

    if not base_path.exists():
        raise FileNotFoundError(f"No singles found for artist {artist}")

    file_path = base_path / (song + ".txt")
    return file_path.read_text(encoding="utf-8")

def load_billboard_song(path: str) -> str:
    file_path = Path("data/lyrics") / path

    if not file_path.exists():
        raise FileNotFoundError(f"Song not found at {path}")

    return file_path.read_text(encoding="utf-8")

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

def load_billboard_year_end(chart: str) -> dict[int, list[dict]]:
    base_path = Path("data/billboard") / chart / "fetched"

    if not base_path.exists():
        raise FileNotFoundError("Chart not found")

    data: dict[int, list[dict]] = {}

    for file_path in sorted(base_path.glob("*.json")):
        if not file_path.stem.isdigit():
            continue

        year = int(file_path.stem)

        year_data = load_billboard_year_metadata(year, chart)

        if year_data is None:
            continue

        songs = year_data.get("songs", [])
        if not songs:
            continue

        valid_songs = [s for s in songs if not s.get("missing", True)]

        if valid_songs:
            data[year] = valid_songs

    if not data:
        raise RuntimeError(f"No years found in {base_path}")

    return data

def load_billboard_year_metadata(
        year: int,
        chart: str,
) -> dict | None:
    path = Path(f"data/billboard/{chart}/fetched/{year}.json")
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)