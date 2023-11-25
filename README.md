# SRT to Speech Script

This Python script converts SRT (SubRip Subtitle) files to speech by using the Google Text-to-Speech (gTTS) API. The script also applies speed adjustments and merges the resulting audio files.

## Prerequisites
- gtts
- pydub
- tqdm

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/JimChr-R4GN4R/subtitles-to-speech
    cd srt-to-speech
    ```

2. Install the required dependencies:

    ```bash
    python3 -m pip install gtts pydub tqdm
    ```

## Usage

Run the script with the following command:

```bash
python3 srt_to_speech.py srt_file language_code
```

### Options
    srt_file: Path to the SRT file.
    language_code: Language code for text-to-speech.

## Example
```bash
python3 srt_to_speech.py example.srt en
```
