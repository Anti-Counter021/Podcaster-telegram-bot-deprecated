import os

import pafy
import pydub


def get_audio(url: str):
    try:
        pafy_obj = pafy.new(url)
    except Exception as _ex:
        return f'{_ex}'

    best_audio = pafy_obj.getbestaudio()
    audio_ext = best_audio.extension

    audio_file_name = f'{pafy_obj.title}.{audio_ext}'

    best_audio.download()

    if audio_ext == 'mp3':
        return f'{audio_file_name} has been downloaded'

    audio = pydub.AudioSegment.from_file(audio_file_name)
    audio.export(f'{pafy_obj.title}.mp3', format='mp3')

    os.remove(os.path.abspath(audio_file_name))

    return f'{pafy_obj.title} has been downloaded'


def main():
    print(get_audio(''))


if __name__ == '__main__':
    main()
