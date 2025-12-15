from genius_lyrics import fetch_album

if __name__ == "__main__":
    artist = input("Artist name: ")
    album = input("Album name: ")
    fetch_album(artist, album)