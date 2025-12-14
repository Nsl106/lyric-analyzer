import re
from collections import Counter

import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

from cli_utils import prompt_artist_album
from data_loading_tools import load_album

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

def pull_words(text: list[str]):
    words = []
    for t in text:
        words.extend(clean_text(t))
    return words

if __name__ == "__main__":
    artist, album = prompt_artist_album()

    text, metadata = load_album(artist, album)
    plot_top_words(pull_words(text), metadata)
