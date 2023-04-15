from aiogram import Bot, Dispatcher, types
from config import TG_USERID
from apis import chat_with_gpt, generate_image, transcribe_audio
import requests
from io import BytesIO


# Holds the previous messages in memory
conversations = {}

def add_initial_system_message(conversation_history):
    initial_message = {"role": "system", "content": "You are a helpful assistant."}
    if not conversation_history or conversation_history[0]["role"] != "system":
        conversation_history.insert(0, initial_message)
    return conversation_history


# The message handler
async def on_message(message: types.Message, bot: Bot):
    global bot_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    my_user_id = int(TG_USERID)
    bot_data = await bot.get_me()
    bot_id = bot_data.id
    mentioned_bot = False

    print(f"Message received from {user_id}")

    # Check and print the content type of the received message
    message_type = message.content_type
    print(f"Message type: {message_type}")

    if user_id == my_user_id:
        print("User is you")
    else:
        try:
            member = await bot.get_chat_member(chat_id, my_user_id)
            if member.status not in ("left", "kicked"):
                print("User shares a group with you")
            else:
                print("User is neither you nor shares a group with you")
                return
        except Exception as e:
            print(f"Error while checking chat member: {e}")
            return

    if message_type == "text":
        mentioned_bot = bot_data.username in message.text
    
    is_direct_reply = (
        message.reply_to_message and message.reply_to_message.from_user.id == bot_id
    )


    if is_direct_reply or mentioned_bot:

        

        if message_type == "voice":
            print("Voice message detected")
            # Get voice file ID and transcribe it
            voice_file_id = message.voice.file_id
            file_info = await bot.get_file(voice_file_id)
            file_path = file_info.file_path
            input_text = await transcribe_audio(file_path)
        else:
            input_text = message.text

        # remove the chatbot tag from the input 
        if mentioned_bot:
            mention = f"@{bot_data.username}"
            input_text = input_text.replace(mention, "").strip()


        # Check for DALL-E image request
        specific_message = "Generate image:"
        if input_text.startswith(specific_message):
            image_prompt = input_text.replace(specific_message, "").strip()

            # Call the DALL-E API
            image_url = await generate_image(image_prompt)

            # Download the image
            response = requests.get(image_url)
            image = BytesIO(response.content)
            image_content = types.InputFile(image, filename="generated_image.png")

            # Send the image to the user
            await message.reply_photo(photo=image_content, caption=f"Generated image for: {image_prompt}")

        else:
            print("text received!")
            # Save the user's message
            if chat_id not in conversations:
                conversations[chat_id] = []
            conversations[chat_id].append({"role": "user", "content": input_text})

            # Call the ChatGPT API with conversation history, including an initial system message
            conversation_history = add_initial_system_message(conversations[chat_id])
            response_text = await chat_with_gpt(conversation_history)

            # Save the bot's response
            conversations[chat_id].append({"role": "assistant", "content": response_text})

            # Print received messages
            print(f"User {user_id} ({message.from_user.first_name}): {input_text}")
            print(f"Bot: {response_text}")

            await message.reply(response_text)
