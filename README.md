# Spotify Music Recommender System

A program that recommends new songs to add to a playlist. The recommender system works based on term frequency. The underlying database is obtained from the "Spotify Million Playlist Dataset Challenge". Since the database only features playlists that were created from 2010 to 2017, the program only works with older songs. This project was developed as an assignment for the Recommender Systems course (2223-KEN3160).

## Functionality Overview
This system operates by scanning playlists containing the same songs, then recommending the most frequently appearing songs across those playlists. To enhance computational efficiency, it utilizes two precomputed hashmaps: one mapping songs to their associated playlists and another indicating song presence within each playlist.

## Installation
1. Clone the repository.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Download the Spotify Million Playlist Dataset from [here](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge).
4. Extract the dataset files into the `data` directory.
5. Run `python file_processor.py`.
6. Run the program using `python main.py`.

## Usage
1. Launch the program by running `python main.py`.
2. Follow the on-screen instructions to select a playlist and receive song recommendations.
3. If you want to connect it to your own spotify account watch this video on how to set it up: 
https://www.youtube.com/watch?v=-FsFT6OwE1A&t=726s

## Contributing
Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).




