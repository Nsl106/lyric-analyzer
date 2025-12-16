from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from analysis_tools import clean_text
from data_loading_tools import load_album, load_billboard_year_end, load_song, load_billboard_song


def main():
    billboard_songs = load_billboard_year_end("year-end-country")

    # keywords = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    # keywords = ["ford", "chevy", "chevrolet", "mustang", "honda", "truck"]
    keywords = ["jack", "daniels", "makers", "bourbon", "turkey", "7", "seven"]
    keywords = ["thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    data = count_words(billboard_songs, keywords)

    plt.figure(figsize=(12, 6))

    print_keywords = [k[0] if isinstance(k, list) else k for k in keywords]
    # print_keywords = [", ".join(k) if isinstance(k, list) else k for k in keywords]
    plt.bar(print_keywords, data)

    plt.title(f"Mentions of words in billboard top country songs from 1970 to 2025")
    plt.tight_layout()
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


def count_words(billboard_songs: dict[int, list[dict]], keywords: list[str | list[str]]) -> list[int]:
    keyword_counts: list[int] = [0] * len(keywords)

    for year, songs in billboard_songs.items():
        song_count = 0

        for i, song in enumerate(songs):
            try:
                lyrics = load_billboard_song(song["lyrics_path"])
                words = clean_text(lyrics)

                for ki, keyword in enumerate(keywords):
                    if isinstance(keyword, str):
                        keyword_counts[ki] += sum(1 for w in words if keyword in w)
                    elif isinstance(keyword, list):
                        for kw in keyword:
                            keyword_counts[ki] += sum(1 for w in words if kw in w)

                song_count += 1
            except Exception as e:
                print(f"({i} {year}) error fetching {title} by {artist} {str(e)}")

    return keyword_counts


if __name__ == "__main__":
    main()
