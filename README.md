# RasPi Display
Displays a variety of information on a screen using SPI on a Raspberry Pi.
The current modules include:
- Daily Athan times depending on the user's set location
- Currently playing Spotify song and Spotify queue

Create a folder called `data` in the root with 2 files named `client.txt` and `locations.txt`.

`client.txt` has 4 lines, the spotify client ID, the spotify client secret, the redirect URI (try `http://localhost:8888/callback`), and the spotify username. Get the spotify username by clicking your icon in the top right of the web app and going to account -> edit-profile. It should be a 28 digit random string.

`locations.txt` takes 3 lines per location. The location name, the latitude coordinates, and the longitude coordinates. I rounded the coordinates to 5 digits, but you can be more or less specific if you'd like.