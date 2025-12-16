import re
from collections import Counter

import matplotlib.pyplot as plt
import nltk
import numpy as np
from nltk.corpus import stopwords

from cli_utils import prompt_artist_album
from data_loading_tools import load_album, load_billboard_year_end, load_song, load_billboard_song
from genius_lyrics import sanitize_filename

nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)


# Removes stopwords and [verse] things
def clean_text(text: str) -> list[str]:
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    words = text.lower().split()

    stops = set(stopwords.words("english"))
    tagged = nltk.pos_tag([w for w in words if w not in stops])
    # tagged = nltk.pos_tag([w for w in words if w not in []])

    boring_filter = ['im']

    # return [word for word, tag in tagged if tag.startswith('NN') and word not in boring_filter]
    # return [word for word, tag in tagged if tag not in ['PRP', 'PRP$'] and word not in boring_filter]
    return [word for word, tag in tagged if word not in boring_filter]


def plot_top_album_words(words, metadata, top_n=30):
    counts = Counter(words)
    most_common = counts.most_common(top_n)

    labels, values = zip(*most_common)

    plt.figure(figsize=(12, 6))
    plt.bar(labels, values)
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top {top_n} Words from {metadata["artist"]} - {metadata["album"]}")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()


def pull_words(text: list[str]):
    words = []
    for t in text:
        words.extend(clean_text(t))
    return words


def main():
    artist, album = prompt_artist_album()

    text, metadata = load_album(artist, album)
    plot_top_album_words(pull_words(text), metadata)

def main2():
    billboard_songs = load_billboard_year_end("year-end-country")

    keywords = ["love", "girl"]
    data = count_word_frequency(billboard_songs, keywords)

    plt.figure(figsize=(12, 6))

    for i, word in enumerate(keywords):
        plot_data(data, i, word)

    plt.title(f"Mentions of words in billboard top country songs from 1970 to 2025")
    plt.ylabel("Count/Song")
    plt.xlabel("Year")
    plt.xticks(np.arange(1970, 2026, 5), rotation=45, ha="right")
    plt.tight_layout()
    plt.legend()
    plt.show()


def plot_data(data: dict[int, list[int]], keyword_index: int, label: str):
    keyword_count = [kws[keyword_index] for kws in list(data.values())]
    x = np.array(list(data.keys()), dtype=float)
    y = np.array(keyword_count, dtype=float)

    window = 9
    y_pad = np.pad(y, (window // 2, window // 2), mode="edge")
    y_smooth = np.convolve(y_pad, np.ones(window) / window, mode="valid")
    plt.plot(x, y_smooth, linewidth=2)
    plt.scatter(x, y, alpha=0.6, label=label)


def count_word_frequency(billboard_songs: dict[int, list[dict]], keywords: list[str]) -> dict[int, list[int]]:
    data = {}

    for year, songs in billboard_songs.items():
        keyword_counts: list[int] = [0] * len(keywords)
        song_count = 0

        for i, song in enumerate(songs):
            try:
                lyrics = load_billboard_song(song["lyrics_path"])
                words = clean_text(lyrics)

                for ki, keyword in enumerate(keywords):
                    keyword_counts[ki] += sum(1 for w in words if keyword in w)

                # keyword_count = sum(1 for w in words if keyword in w)
                # year_mentions += keyword_count

                song_count += 1
            except Exception as e:
                print(f"({i} {year}) error fetching {title} by {artist} {str(e)}")

        data[year] = [x / song_count for x in keyword_counts]

    return data


if __name__ == "__main__":
    main2()
