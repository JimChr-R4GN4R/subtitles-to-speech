from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.effects import speedup
import re
from datetime import datetime, timedelta
import wave
from tqdm import tqdm
from typing import List
import argparse

def merge_wavs(wavs_list: List[str], outfile: str) -> None:
    data = [(wave.open(infile, 'rb').getparams(), wave.open(infile, 'rb').readframes(wave.open(infile, 'rb').getnframes())) for infile in wavs_list]
    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    output.writeframes(b''.join([d[1] for d in data]))
    output.close()

def time_to_milliseconds(time_str: str) -> int:
    return int((datetime.strptime(time_str, "%H:%M:%S,%f") - datetime(1900, 1, 1)).total_seconds() * 1000)

def seconds_to_milliseconds(time_seconds: float) -> int:
    return int(timedelta(seconds=time_seconds).total_seconds() * 1000)

def delay(wav_file: str, ms: int) -> None:
    silence = AudioSegment.silent(duration=ms)
    old_sound = AudioSegment.from_wav(wav_file)
    new_sound = silence + old_sound
    new_sound.export(wav_file, format="wav")

def from_text_to_speech(filename: str, text: str, language: str) -> None:
    output_file = f'{filename}'
    gTTS(text=text, lang=language, slow=False).save(f'{output_file}.mp3')
    AudioSegment.from_mp3(f'{output_file}.mp3').export(f'{output_file}.wav', format="wav")
    os.remove(f'{output_file}.mp3')

def speed_up_audio(input_path: str, period_start: int, period_end: int, fade_duration: int = 100) -> None:
    audio = AudioSegment.from_wav(input_path)
    original_period, period_duration = seconds_to_milliseconds(audio.duration_seconds), period_end - period_start
    if original_period < period_duration:
        return
    speed_factor = original_period / period_duration
    sped_up_audio = audio.speedup(playback_speed=speed_factor)
    sped_up_audio = sped_up_audio.fade_in(duration=fade_duration).fade_out(duration=fade_duration)
    sped_up_audio.export(input_path, format="wav")

def srt_to_speech(srt_file: str, language: str = 'en') -> None:
    my_srt = open(srt_file, 'r', encoding='utf-8').read()
    pattern = re.compile(r"(\d+)\n(\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+)\s+(.+)")
    matches = pattern.findall(my_srt)

    for id_, match in enumerate(tqdm(matches)):
        number, period, text = int(match[0]), match[1], match[2]
        period_start, period_end = [time_to_milliseconds(i) for i in period.split(' --> ')]
        if number == 1:
            from_text_to_speech(number, match[2], language)
            speed_up_audio(f"{number}.wav", period_start, period_end)
            delay(f"{number}.wav", period_start)
        else:
            prev_match = matches[id_ - 1]
            prev_period_start, prev_period_end = [time_to_milliseconds(i) for i in prev_match[1].split(' --> ')]
            from_text_to_speech(number, match[2], language)
            speed_up_audio(f"{number}.wav", period_start, period_end)
            delay(f"{number}.wav", period_start - prev_period_end)

    numbers_list = [f'{match[0]}.wav' for match in matches]
    merge_wavs(numbers_list, 'final.wav')
    [os.remove(i) for i in numbers_list]

def parse_args():
    parser = argparse.ArgumentParser(description='Convert SRT file to speech.')
    parser.add_argument('srt_file', type=str, help='Path to the SRT file')
    parser.add_argument('language', type=str, help='Language code for text-to-speech')
    return parser.parse_args()

def main():
    args = parse_args()
    srt_to_speech(args.srt_file, args.language)

if __name__ == "__main__":
    main()
