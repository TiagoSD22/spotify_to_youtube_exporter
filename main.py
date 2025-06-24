import argparse
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# --- Environment Setup ---
# To run this script, you need to set up your Spotify API credentials as
# environment variables.
#
# 1. Go to the Spotify Developer Dashboard: https://developer.spotify.com/dashboard/
# 2. Create an application to get your Client ID and Client Secret.
# 3. Set the following environment variables in your system:
#    - SPOTIPY_CLIENT_ID: Your Spotify application's Client ID.
#    - SPOTIPY_CLIENT_SECRET: Your Spotify application's Client Secret.
#
# For Windows:
# setx SPOTIPY_CLIENT_ID "your_client_id"
# setx SPOTIPY_CLIENT_SECRET "your_client_secret"
#
# For macOS/Linux:
# export SPOTIPY_CLIENT_ID='your_client_id'
# export SPOTIPY_CLIENT_SECRET='your_client_secret'
#
# Remember to restart your terminal or IDE after setting these variables.

def get_playlist_tracks(playlist_url):
    """
    Retrieves the track names from a Spotify playlist.

    Args:
        playlist_url (str): The URL of the Spotify playlist.

    Returns:
        list: A list of track names (artist and song name).
    """
    try:
        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        playlist_id = playlist_url.split("/")[-1].split("?")[0]
        results = sp.playlist_tracks(playlist_id)
        tracks = []
        for item in results['items']:
            track = item['track']
            if track:
                track_name = f"{track['artists'][0]['name']} - {track['name']}"
                tracks.append(track_name)
        return tracks
    except Exception as e:
        print(f"Error retrieving playlist tracks: {e}")
        return []

def search_youtube(song_title):
    """
    Searches YouTube for a given song title and returns the URL of the first result.

    Args:
        song_title (str): The title of the song to search for.

    Returns:
        str: The URL of the first YouTube search result, or None if not found.
    """
    try:
        search_query = f"{song_title} official music video"
        search_url = f"https://www.youtube.com/results?search_query={requests.utils.quote(search_query)}"
        response = requests.get(search_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith("/watch?v="):
                return f"https://www.youtube.com{href}"
    except requests.exceptions.RequestException as e:
        print(f"Error making request to YouTube: {e}")
    except Exception as e:
        print(f"An error occurred while searching YouTube: {e}")
    return None

def main():
    """
    Main function to parse arguments and find YouTube links for a Spotify playlist.
    """
    parser = argparse.ArgumentParser(description="Find YouTube links for songs in a Spotify playlist.")
    parser.add_argument("playlist_url", help="The URL of the Spotify playlist.")
    args = parser.parse_args()

    tracks = get_playlist_tracks(args.playlist_url)
    if not tracks:
        print("Could not retrieve any tracks from the playlist.")
        return

    youtube_links = {}
    for track in tracks:
        print(f"Searching for: {track}")
        youtube_link = search_youtube(track)
        if youtube_link:
            youtube_links[track] = youtube_link
            print(f"  Found: {youtube_link}")
        else:
            print("  Could not find a YouTube link.")

    print("\n--- All YouTube Links ---")
    for track, link in youtube_links.items():
        print(f"{track}: {link}")

if __name__ == "__main__":
    main()
