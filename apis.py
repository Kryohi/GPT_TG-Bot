import asyncio
import openai
import requests
from io import BytesIO
from config import OPENAI_API_KEY

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


async def generate_image(prompt):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
    )

    # Get the image URL
    image_url = response['data'][0]['url']  # response.choices[0].image_url
    return image_url


# Audio message support
async def transcribe_audio(file_id):
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}"

    # Download the voice file
    response = requests.get(file_url)

    # Save the voice file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio.write(response.content)
        temp_audio_filename = temp_audio.name

    # Call the Whisper ASR API
    with open(temp_audio_filename, "rb") as audio_file:
        response = openai.Speech.create(
            engine="whisper",
            file=audio_file,
            language="en-US",
            sample_rate=16000,
        )

    # Delete the temporary voice file
    os.unlink(temp_audio_filename)

    # Get the transcribed text
    transcribed_text = response["choices"][0]["text"]
    return transcribed_text

