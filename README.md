# RasPi Display
Displays a variety of information on a screen using SPI on a Raspberry Pi.
The current modules include:
- Current system information including CPU temps, RAM and disk usage, and network speeds
- Daily Athan times depending on the user's set location
- Currently playing Spotify song ~~and Spotify queue~~ (Fetching the queue is locked to Spotify Premium)
- Weather forecast for the user's set location

Each module also includes a number of substates:
- The system information module has substates with more in depth information on the CPU, RAM, Disk, and Network
- The Athan and Weather modules have a substate for each location that is set by the user
- The Spotify module has a substate that shows a list of previously played songs

The currently showing module and substate can be changed by tapping the screen. The top half of the screen changes the module, while the bottom half of the screen changes the substate.

## How to set it up

Create a folder called `data` in the root with 2 files named `client.txt` and `locations.txt`.

`client.txt` has 4 lines, the spotify client ID, the spotify client secret, the redirect URI (try `http://localhost:8888/callback`), and the spotify username. Get the spotify username by clicking your icon in the top right of the web app and going to account -> edit-profile. It should be a 28 digit random string.

`locations.txt` takes 3 lines per location. The location name, the latitude coordinates, and the longitude coordinates. I rounded the coordinates to 5 digits, but you can be more or less specific if you'd like.
