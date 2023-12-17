import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# def save_html_with_selenium(url, file_name):
#     # Set up the Selenium WebDriver
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service)

#     driver.get(url)
#     time.sleep(10)  # Wait for the page to load completely

#     # Save the page source to a file
#     with open(file_name, 'w', encoding='utf-8') as file:
#         file.write(driver.page_source)
    
#     print(f"HTML content saved to {file_name}")
#     driver.quit()

# # Example usage
# url = 'https://www.1001tracklists.com/tracklist/2frtqjx9/tiesto-tiestos-club-life-871-2023-12-09.html'
# save_html_with_selenium(url, 'C:\\Users\\kilan\\IDrive-Sync\\Documents\\Coding\\tiesto-spotify-playlist\\tiesto_club_life_871.html')


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
file_path = 'C:\\Users\\kilan\\IDrive-Sync\\Documents\\Coding\\tiesto-spotify-playlist\\tiesto_club_life_871.html'  # Replace with the local path to your HTML file
songs_list = get_songs_from_set(file_path)
for song in songs_list:
    print(song)