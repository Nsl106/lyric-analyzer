import json
from pathlib import Path

from data_loading_tools import load_billboard_year_end, load_song, load_billboard_year_metadata
from genius_lyrics import fetch_song

if __name__ == "__main__":
    chart = "year-end-country"
    billboard_songs = load_billboard_year_end(chart)

    output_dir = Path(f"data/billboard/{chart}/fetched")
    output_dir.mkdir(parents=True, exist_ok=True)

    for year, songs in billboard_songs.items():
        print(f"\n=== {year} ===")

        existing = load_billboard_year_metadata(year, chart)

        if existing:
            print(f"\nResuming {year}...")
            records = existing["songs"]
            by_rank = {r["rank"]: r for r in records}
        else:
            print(f"\nStarting {year}...")
            records = []
            by_rank = {}


        for song in songs:
            rank = song["rank"]

            record = by_rank.get(rank)

            if record and not record.get("missing", True):
                continue

            if not record:
                record = {
                    "rank": song["rank"],
                    "searched_artist": song["artist"],
                    "searched_title": song["title"],
                    "missing": True,
                }
                records.append(record)

            try:
                result = fetch_song(song["artist"], song["title"])
                record.update(result)
            except Exception as e:
                record["error"] = str(e)
                print(f"error fetching {song["title"]} by {song['artist']} (#{song["rank"]} in {year})")


        out_path = output_dir / f"{year}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "year": year,
                    "chart": chart,
                    "total_songs": len(records),
                    "fetched": sum(not r["missing"] for r in records),
                    "songs": records,
                },
                f,
                indent=2,
            )

        print(
            f"Saved {year}: "
            f"{sum(not r['missing'] for r in records)} / {len(records)}"
        )