import re

import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)

# Removes stopwords and [verse] things
def clean_text(text: str, clear_stopwords: bool=True) -> list[str]:
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    words = text.lower().split()

    stops = set(stopwords.words("english"))

    no_stops = [w for w in words if w not in stops]
    # tagged = nltk.pos_tag([w for w in words if w not in stops])

    boring_filter = ['im']

    if clear_stopwords:
        return [word for word in no_stops if word not in boring_filter]
    else:
        return [word for word in words if word not in boring_filter]
    # return [word for word, tag in tagged if tag.startswith('NN') and word not in boring_filter]
    # return [word for word, tag in tagged if tag not in ['PRP', 'PRP$'] and word not in boring_filter]
