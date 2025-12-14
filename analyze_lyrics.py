import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from prompt_toolkit.completion import FuzzyCompleter

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from cli_utils import ArtistCompleter, AlbumCompleter

history = FileHistory(".cli_history")

nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)


def clean_text(text: str) -> list[str]:
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    words = text.lower().split()

    stops = set(stopwords.words("english"))
    tagged = nltk.pos_tag([w for w in words if w not in stops])
    return [word for word, tag in tagged if tag.startswith('NN')]
    # return [word for word, tag in tagged if tag not in ['PRP', 'PRP$']]


def load_album(artist: str, album: str) -> tuple[list[Any], dict]:
    artist = artist.replace(" ", "_")
    album = album.replace(" ", "_")

    base_path = Path("data/lyrics") / artist / album

    if not base_path.exists():
        raise FileNotFoundError("Album not cached yet")

    metadata = load_metadata(artist, album)

    words = []

    for track in metadata["tracks"]:
        file_path = base_path / track["filename"]
        text = file_path.read_text(encoding="utf-8")
        words.extend(clean_text(text))


    return words, metadata

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

def plot_top_words(words, metadata, top_n=50):
    counts = Counter(words)
    most_common = counts.most_common(top_n)

    labels, values = zip(*most_common)

    plt.figure(figsize=(12, 6))
    plt.bar(labels, values)
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top {top_n} Words from {metadata["artist"]} - {metadata["album"]}")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    artist = prompt(
        "Artist: ",
        completer=FuzzyCompleter(ArtistCompleter()),
        history=history
    )

    album = prompt(
        "Album: ",
        completer=FuzzyCompleter(AlbumCompleter(artist)),
        history=history
    )

    words, metadata = load_album(artist, album)
    plot_top_words(words, metadata)
