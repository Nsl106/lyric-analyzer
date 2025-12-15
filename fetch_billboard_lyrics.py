from data_loading_tools import load_billboard_year_end, load_song
from genius_lyrics import fetch_song

if __name__ == "__main__":
    billboard_songs = load_billboard_year_end("year-end-country")

    for year, songs in billboard_songs.items():
        if year < 1996:
            continue
        for i, song in enumerate(songs):
            if year == 1996 and i < 66:
                continue
            print(f"({i}/{len(songs)})@{year} fetching {song["title"]} by {song['artist']}")
            try:
                fetch_song(song["artist"], song["title"])
            except ValueError:
                print(f"error fetching {song["title"]}")