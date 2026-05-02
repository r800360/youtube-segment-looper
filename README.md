# YouTube Segment Looper

A small Python desktop app for looping a specific segment of a YouTube video.

Paste a YouTube URL, enter a start time and end time, and the app opens `mpv` to loop only that section. This is useful for music, studying, transcription, practice loops, background audio, and replaying a favorite part of a long video.

## Features

- Loop any YouTube segment between a chosen start and end timestamp
- Supports time formats like:
  - `90`
  - `1:30`
  - `01:02:03`
- Optional audio-only mode
- Simple desktop GUI using `customtkinter`
- Uses `mpv` for reliable playback
- Uses `yt-dlp` support through `mpv` for YouTube streaming
- Includes a Stop Playback button to close active `mpv` playback

## Demo Workflow

1. Open the app.
2. Paste a YouTube URL.
3. Enter a start time.
4. Enter an end time.
5. Click **Loop Segment**.
6. The selected segment loops in `mpv`.

Example:

```text
URL:   https://www.youtube.com/watch?v=VIDEO_ID
Start: 0:43
End:   1:12
```

## Project Structure

```text
youtube-segment-looper/
│
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

### Python

Recommended:

```text
Python 3.11 or Python 3.12
```

Python 3.11 is a safe default.

### Python Packages

The app uses:

```text
customtkinter
```

### External Tools

You also need these installed on your computer:

- `mpv`
- `yt-dlp`

`mpv` handles playback and looping.  
`yt-dlp` allows `mpv` to access YouTube video/audio streams.

## Windows Setup

These instructions assume Windows PowerShell.

### 1. Clone or create the project folder

```powershell
cd C:\Users\YOUR_USERNAME\Documents
mkdir youtube-segment-looper
cd youtube-segment-looper
```

Place `main.py` and `requirements.txt` inside this folder.

### 2. Create a virtual environment

```powershell
py -3.11 -m venv .venv
```

If Python 3.11 is not installed, you can use your default Python:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see something like this at the start of your prompt:

```powershell
(.venv) PS C:\Users\YOUR_USERNAME\Documents\youtube-segment-looper>
```

### 4. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### 5. Install Python dependencies

```powershell
pip install -r requirements.txt
```

If you do not have `requirements.txt`, install manually:

```powershell
pip install customtkinter
```

## Installing mpv and yt-dlp on Windows

### Install yt-dlp

```powershell
winget install --id yt-dlp.yt-dlp -e
```

Check that it works:

```powershell
yt-dlp --version
```

### Install mpv

Recommended winget package:

```powershell
winget install --id shinchiro.mpv -e
```

Check that it works:

```powershell
mpv --version
```

If `mpv --version` works, you are ready.

## Running the App

From the project folder:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Daily use after setup:

```powershell
cd C:\Users\YOUR_USERNAME\Documents\youtube-segment-looper
.\.venv\Scripts\Activate.ps1
python main.py
```

## Example `requirements.txt`

```text
customtkinter
```

## Troubleshooting

### `mpv` is not recognized

You may see:

```powershell
mpv : The term 'mpv' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

This means Windows cannot find `mpv.exe` through PATH.

First, check if mpv is installed:

```powershell
winget list mpv
```

If you see something like:

```text
MPV Player    shinchiro.mpv
```

then mpv is installed, but PATH may be wrong.

### Find the mpv executable

Common location:

```text
C:\Program Files\MPV Player\mpv.exe
```

Check it directly:

```powershell
Test-Path "C:\Program Files\MPV Player\mpv.exe"
```

If this returns:

```powershell
True
```

then mpv exists.

### Correct PATH setup

PATH should contain the folder:

```text
C:\Program Files\MPV Player
```

not the file:

```text
C:\Program Files\MPV Player\mpv.exe
```

To fix PATH, run:

```powershell
$wrongPath = "C:\Program Files\MPV Player\mpv.exe"
$correctPath = "C:\Program Files\MPV Player"

$userPathParts = [Environment]::GetEnvironmentVariable("Path", "User") -split ";"

$cleanedPathParts = $userPathParts |
    Where-Object { $_ -and $_ -ne $wrongPath -and $_ -ne $correctPath }

$newUserPath = ($cleanedPathParts + $correctPath) -join ";"

[Environment]::SetEnvironmentVariable("Path", $newUserPath, "User")

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

Then test:

```powershell
where.exe mpv
mpv --version
```

If that works, the app can use:

```python
"mpv"
```

inside the Python command list.

### Direct mpv path workaround

If PATH continues to be annoying, you can hardcode the full path in `main.py`.

Change:

```python
command = [
    "mpv",
```

to:

```python
command = [
    r"C:\Program Files\MPV Player\mpv.exe",
```

This bypasses PATH completely.

### `yt-dlp` works but mpv does not

This is normal if only `yt-dlp` was added to PATH correctly. `yt-dlp` and `mpv` are installed separately.

Check:

```powershell
yt-dlp --version
mpv --version
```

If `yt-dlp` works but `mpv` fails, fix the mpv PATH issue above.

### PowerShell activation error

If activating the virtual environment gives an execution policy error, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## How the App Works

The Python app builds a command like this:

```powershell
mpv "https://www.youtube.com/watch?v=VIDEO_ID" --start=83 --ab-loop-a=83 --ab-loop-b=167 --force-window=yes --no-video
```

Where:

- `--start` starts playback at the selected timestamp.
- `--ab-loop-a` sets the loop start point.
- `--ab-loop-b` sets the loop end point.
- `--no-video` enables audio-only mode.
- `--force-window=yes` keeps an mpv window available.

## Notes on YouTube URLs

The app should work with standard YouTube URLs such as:

```text
https://www.youtube.com/watch?v=VIDEO_ID
```

and shortened URLs such as:

```text
https://youtu.be/VIDEO_ID
```

If a video fails to load, try updating `yt-dlp`:

```powershell
yt-dlp -U
```

or reinstalling with winget:

```powershell
winget upgrade --id yt-dlp.yt-dlp -e
```

## Future Improvements

Possible next features:

- Save favorite loops
- Load saved loops from a JSON file
- Named playlists
- Keyboard shortcuts
- Playback speed control
- Local video/audio file support
- Export/import loop presets
- System tray mode
- Better error messages
- Recently played history
- Dark/light theme toggle
- One-click GitHub release packaging

Example future loop preset format:

```json
[
  {
    "name": "Favorite chorus",
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "start": "1:14",
    "end": "1:42",
    "audio_only": true
  }
]
```

## Disclaimer

This project is a personal playback helper. It does not download or redistribute YouTube videos by default. It simply launches `mpv` to stream and loop the selected segment locally.

Make sure your usage follows YouTube's terms of service and applicable copyright rules.

## License

MIT License is a good default if you want others to freely use, modify, and share the project.

If you want to add a license file, create a `LICENSE` file containing the MIT License text.
