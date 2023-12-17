import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
episode = "870"

def save_html_with_selenium(url, file_name):
    # Set up the Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    time.sleep(5)  # Wait for the page to load completely

    # Save the page source to a file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    
    print(f"HTML content saved to {file_name}")
    driver.quit()

# Example usage
url = 'https://www.1001tracklists.com/tracklist/2sxdnp5t/tiesto-tiestos-club-life-870-2023-12-02.html'
save_html_with_selenium(url, f'C:\\Users\\kilan\\IDrive-Sync\\Documents\\Coding\\tiesto-spotify-playlist\\tiesto_club_life_{episode}.html')


def get_songs_from_set(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    # Find meta tags for song names and artists
    track_names = soup.find_all('meta', {'itemprop': 'name'})
    artists = soup.find_all('meta', {'itemprop': 'byArtist'})

    songs = []
    for name, artist in zip(track_names, artists):
        song_name = name['content'] if name and 'content' in name.attrs else ''
        artist_name = artist['content'] if artist and 'content' in artist.attrs else ''
        song = f"{artist_name} - {song_name}" if artist_name and song_name else ''
        if song:
            songs.append(song)
    
    return songs

# Example usage
file_path = f'C:\\Users\\kilan\\IDrive-Sync\\Documents\\Coding\\tiesto-spotify-playlist\\tiesto_club_life_{episode}.html'  # Replace with the local path to your HTML file
songs_list = get_songs_from_set(file_path)
for song in songs_list:
    print(song)

def create_spotify_playlist(songs, playlist_name):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="9d60446d0d8f495bb77f3e78da709dc3",
                                                   client_secret="7b6695c2a30b4bdb9d9dba790e97e0b4",
                                                   redirect_uri="http://localhost:8888/callback",
                                                   scope="playlist-modify-public"))

    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name)
    track_ids = []  # Fetch track IDs based on song names

    for song in songs:
        results = sp.search(q=song, limit=1, type='track')
        tracks = results['tracks']['items']
        if tracks:
            track_ids.append(tracks[0]['id'])

    sp.playlist_add_items(playlist['id'], track_ids)

create_spotify_playlist(songs_list, f'Tiesto Club Life {episode}')
