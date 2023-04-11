# CharlesBot

CharlesBot is a Telegram bot that leverages the OpenAI API to chat with users and generate images using the DALL-E model. You can start a conversation by sending a text message or requesting an image by sending a message starting with "Generate image:" followed by the image description.

## Requirements

- Python 3.6+
- aiogram
- openai

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Kryohi/GPT_TG-Bot.git
cd GPT_TG-Bot
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate    # On Windows use 'venv\Scripts\activate'
```

3. Install the required packages:

```bash
pip install --user aiogram openai
```

4. Set up the environment variables with your OpenAI API key, Telegram Bot API key, and your Telegram user ID:

```bash
export OPENAI_API_KEY="your_openai_api_key"
export TELEGRAM_API_KEY_CHATBOT="your_telegram_bot_api_key"
export TG_USERID="your_telegram_user_id"

# On Windows use 'set' instead of 'export':
# set OPENAI_API_KEY="your_openai_api_key"
# set TELEGRAM_API_KEY_CHATBOT="your_telegram_bot_api_key"
# set TG_USERID="your_telegram_user_id"
```

If you don't know how to create a Telegram bot and obtain its API key, follow the instructions in the [Telegram BotFather documentation](https://core.telegram.org/bots#botfather). For the OpenAI API keys: https://platform.openai.com/account/api-keys.

## Usage

To start the bot, run:

```bash
python main.py
```

To interact with the bot, send a message to your bot on Telegram or add the bot to a group. The bot will respond to any message that mentions it or is a direct reply to one of its messages.

To request an image, send a message starting with "Generate image:" followed by the description. For instance:

```
Generate image: a beautiful mountain landscape
```

The bot will generate and send back an image based on the description.

## Future Development

- [ ] Use different models to generate images (Stable Diffusion?)
- [ ] Fix audio transcription.
- [ ] Access to the web.
- [ ] PineCone integration.

## License

This project is licensed under the terms of the MIT License.
