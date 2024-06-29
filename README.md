# MP3 Tag Editor

A Tkinter-based MP3 tag editor with file browsing and renaming capabilities.

## Prerequisites

- Python 3.6+
- pip

## Installation

1. Clone the repository in the desired folder:
```
git clone https://github.com/GreyLilac09/mp3-tagger.git
cd mp3-tagger
```

2. Install required dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python mp3-tagger.py
```

If you get the message `Tkinter: "Python may not be configured for Tk"`, run this command: `brew install python-tk`

## Features

- Browse and select MP3 files using a tree view
- View and edit MP3 tags (Title, Artist, Album)
- Auto-parse file names to extract artist and title information. The file name should be in the format `ARTIST - SONG_NAME.mp3`
- Rename MP3 files
- Update MP3 tags

## Development

The application is built using:
- Tkinter for the GUI
- mutagen for MP3 tag manipulation

Key files:
- `mp3_tag_editor.py`: Main application script

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.