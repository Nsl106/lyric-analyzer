import json
from datetime import date
from pathlib import Path

import billboard


START_YEAR = 1970
END_YEAR = date.today().year


def fetch_year(year: int) -> list[dict]:
    chart = billboard.ChartData("hot-country-songs", year=year)

    entries = []
    for entry in chart.entries:
        entries.append({
            "rank": entry.rank,
            "title": entry.title,
            "artist": entry.artist
        })

    return entries


def main():
    output_dir = Path("data/billboard/year-end-country")
    output_dir.mkdir(parents=True, exist_ok=True)

    all_years = {}

    for year in range(START_YEAR, END_YEAR + 1):
        print(f"Fetching year-end country chart for {year}...")
        songs = fetch_year(year)

        all_years[year] = songs

        with open(output_dir / f"{year}.json", "w", encoding="utf-8") as f:
            json.dump(songs, f, indent=2)

if __name__ == "__main__":
    main()
