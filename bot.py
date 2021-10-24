import os

import dotenv
import pafy
import pydub
from aiogram import Bot, Dispatcher, executor, types

dotenv.load_dotenv('config.env')

TOKEN = os.environ.get('TOKEN')

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f'Hello {message.from_user.username}! I\'m PodcasterBot!')


@dispatcher.message_handler(content_types=['text'])
async def send_audio(message: types.Message):
    try:
        pafy_obj = pafy.new(message.text)
        await message.answer('Please waiting...')

        title = pafy_obj.title

        best_audio = pafy_obj.getbestaudio()
        audio_ext = best_audio.extension
        audio_file_name = f'{title}.{audio_ext}'

        best_audio.download()

        if audio_ext == 'mp3':
            with open(audio_file_name, 'rb') as file:
                await bot.send_audio(message.chat.id, audio=file)
        else:
            audio = pydub.AudioSegment.from_file(audio_file_name)
            audio.export(f'{title}.mp3', format='mp3')

            with open(f'{title}.mp3', 'rb') as file:
                await bot.send_audio(message.chat.id, audio=file)

            os.remove(os.path.abspath(f'{title}.mp3'))
        os.remove(os.path.abspath(audio_file_name))
    except Exception as _ex:
        await message.answer('Please check URL')


if __name__ == '__main__':
    executor.start_polling(dispatcher)
