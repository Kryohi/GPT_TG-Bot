import os
import tempfile
from aiogram import Bot
import asyncio
import openai
import requests
from io import BytesIO
from config import OPENAI_API_KEY, TELEGRAM_API_KEY_CHATBOT

openai.api_key = OPENAI_API_KEY

# Function to call the ChatGPT API
async def chat_with_gpt(conversation_history):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history,
        )
    )

    response_text = response.choices[0].message.content
    return response_text


# Async function to call the updated API for image generation
async def generate_image(prompt):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
    )

    # Get the image URL
    image_url = response['data'][0]['url']
    return image_url


import soundfile as sf
from pydub import AudioSegment

# Function to call the Whisper API and return the transcribed text
async def transcribe_audio(file_path):
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_API_KEY_CHATBOT}/{file_path}"

    # Download the voice file
    response = requests.get(file_url)

    # Save the temporary voice file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".oga") as temp_audio:
        temp_audio.write(response.content)
        temp_audio_filename = temp_audio.name

    # Convert the audio format to WAV
    audio = AudioSegment.from_ogg(temp_audio_filename)
    converted_audio_filename = os.path.splitext(temp_audio_filename)[0] + ".wav"
    audio.export(converted_audio_filename, format="wav")

    print("Calling the Whisper API to transcribe the message...")

    # Call the OpenAI API
    with open(converted_audio_filename, "rb") as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)

    # Delete the temporary voice files
    os.unlink(temp_audio_filename)
    os.unlink(converted_audio_filename)

    # Get the transcribed text
    transcribed_text = response["text"]

    return transcribed_text
