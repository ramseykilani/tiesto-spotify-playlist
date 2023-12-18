##### Imports #########
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import configparser
from datetime import datetime, timedelta

##### Function ##########

def save_html_with_selenium(url, file_name):
    # Set up the Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get(url)
    time.sleep(3)  # Wait for the page to load completely

    # Save the page source to a file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    
    print(f"HTML content saved to {file_name}")
    driver.quit()

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

def get_episode_url(episode_number):
    with open('C:\\Users\\kilan\\IDrive-Sync\\Documents\\Coding\\tiesto-spotify-playlist\\HTMLs\\index.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Search for the episode link
    episode_link = None
    links = soup.find_all('a')
    for link in links:
        if link.text.strip() == f"Tiësto - Club Life {episode_number}":
            episode_link = link.get('href')
            break

    return episode_link

def create_spotify_playlist(songs, playlist_name,client_id,client_secret):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
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

####### Code ###########

config = configparser.ConfigParser()
config.read('C:\\Users\\kilan\\IDrive-Sync\\Documents\\Coding\\tiesto-spotify-playlist\\config.ini')

client_id = config['spotify']['client_id']
client_secret = config['spotify']['client_secret']
episode_number = "867"
episode_html_path = f'C:\\Users\\kilan\\IDrive-Sync\\Documents\\Coding\\tiesto-spotify-playlist\\HTMLs\\tiesto_club_life_{episode_number}.html'

# Save index file
index_url = 'https://www.1001tracklists.com/source/6wndmv/tiestos-club-life/index.html'
index_path = 'C:\\Users\\kilan\\IDrive-Sync\\Documents\\Coding\\tiesto-spotify-playlist\\HTMLs\\index.html'
save_html_with_selenium(index_url, index_path)

# Get current episode url
episode_url = get_episode_url(int(episode_number))
print(episode_url)

# Get episode song list
if episode_url:
    full_url = 'https://www.1001tracklists.com' + episode_url  # Assuming the fetched URL is relative
    # save_html_with_selenium(full_url, episode_html_path)
    songs_list = get_songs_from_set(episode_html_path)
    for song in songs_list:
        print(song)
else:
    print(f"Episode {episode_number} not found.")

# Create playlist from list
create_spotify_playlist(songs_list, f'Tiesto Club Life {episode_number}',client_id,client_secret)
