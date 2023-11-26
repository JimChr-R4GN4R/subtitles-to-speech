# SRT to Speech Script

This Python script leverages the gTTS API to transform SRT (SubRip Subtitle) files into spoken audio. Beyond simple conversion, the script incorporates intelligent speed adjustments, ensuring that the synthesized speech aligns closely with the pacing of the original speaker for a more natural and synchronized playback experience. 

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
python3 srt_to_speech.py srt_file output_file language_code
```

### Options
    srt_file: Path to the SRT file.
    output_file: Output filename.
    language_code: Language code for text-to-speech.

## Example
```bash
python3 srt_to_speech.py example.srt output.wav en
```
