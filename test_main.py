import unittest
from unittest.mock import patch
import main

class TestSpotifyToYouTube(unittest.TestCase):
    def setUp(self):
        # Example tracks as would be returned from a playlist
        self.tracks = [
            "Daft Punk - One More Time",
            "Queen - Bohemian Rhapsody"
        ]

    @patch('main.get_playlist_tracks')
    @patch('main.search_youtube')
    def test_youtube_links_for_playlist(self, mock_search_youtube, mock_get_playlist_tracks):
        # Mock the playlist tracks
        mock_get_playlist_tracks.return_value = self.tracks
        # Mock YouTube search results
        mock_search_youtube.side_effect = [
            "https://www.youtube.com/watch?v=FGBhQbmPwH8",
            "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"
        ]

        # Simulate argument parsing
        with patch('argparse.ArgumentParser.parse_args', return_value=type('', (), {'playlist_url': 'dummy_url'})()):
            with patch('builtins.print') as mock_print:
                main.main()
                # Check that the YouTube links were printed
                mock_print.assert_any_call('Searching for: Daft Punk - One More Time')
                mock_print.assert_any_call('  Found: https://www.youtube.com/watch?v=FGBhQbmPwH8')
                mock_print.assert_any_call('Searching for: Queen - Bohemian Rhapsody')
                mock_print.assert_any_call('  Found: https://www.youtube.com/watch?v=fJ9rUzIMcZQ')
                mock_print.assert_any_call('\n--- All YouTube Links ---')
                mock_print.assert_any_call('Daft Punk - One More Time: https://www.youtube.com/watch?v=FGBhQbmPwH8')
                mock_print.assert_any_call('Queen - Bohemian Rhapsody: https://www.youtube.com/watch?v=fJ9rUzIMcZQ')

if __name__ == "__main__":
    unittest.main()
