# AI Chatbot with Token Tracking

A simple command-line chatbot built in Python that talks to the [Groq API](https://groq.com/) using the OpenAI-compatible SDK. It keeps the conversation history so the bot remembers context, and it shows how many tokens each request uses.

## Features

- Chat with an AI model right from your terminal
- Remembers the conversation (full message history is sent on every request)
- Shows token usage after every response (prompt, completion, total)
- Shows a session summary when you exit
- Handles errors gracefully (rate limits, connection issues, API errors)
- Clean exit with `quit`, `exit`, or `Ctrl + C`

## Requirements

- Python 3.8 or higher
- A free Groq API key from [console.groq.com](https://console.groq.com/keys)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **(Optional) Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies**

   ```bash
   pip install openai python-dotenv
   ```

4. **Set up your API key**

   Create a file named `.env` in the project folder and add:

   ```
   GROQ_API_KEY=your_api_key_here
   ```

   > ⚠️ Never upload your `.env` file to GitHub. Add `.env` to your `.gitignore` so your key stays private.

## Usage

Run the script (replace `chatbot.py` with your file name):

```bash
python chatbot.py
```

Then just type your message at the **Ask Something** prompt. To leave, type `quit` or `exit`.

## Example

```
AI CHATBOT
Type 'quit' or 'exit' to terminate the conversation.
----------------------------------------

Ask Something: What is Python?

Bot: Python is a popular, beginner-friendly programming language...

========================================
TOKEN USAGE - CURRENT REQUEST
========================================
Prompt Tokens     : 42
Completion Tokens : 118
Total Tokens      : 160
========================================

Ask Something: exit

Exiting the chatbot. Goodbye!

========================================
CHAT SESSION SUMMARY
========================================
Total API Requests       : 1
Total Prompt Tokens      : 42
Total Completion Tokens  : 118
Total Tokens Consumed    : 160
========================================
```

## How It Works

1. Loads the API key from the `.env` file.
2. Creates an OpenAI-compatible client pointed at Groq's API.
3. Stores the system prompt and every message in a `messages` list.
4. On each turn, sends the full history to the model, prints the reply, and updates the token counters.
5. If a request fails, the last user message is removed so the history stays clean.

## Configuration

You can change these values at the top of the script:

| Setting | Description | Default |
|---------|-------------|---------|
| `MODEL` | The Groq model to use | `openai/gpt-oss-120b` |
| System prompt | The bot's instructions/personality | `You are a helpful assistant.` |

## Project Structure

```
.
├── chatbot.py      # Main script
├── .env            # Your API key (do not commit!)
├── .gitignore      # Should include .env
└── README.md
```

## Possible Improvements

- Trim old messages to keep token usage low in long chats
- Wrap the logic in a class instead of using global variables
- Add streaming so replies appear word by word
- Save chat history to a file

## License

This project is open source. Feel free to use and modify it. Add a license of your choice (for example, MIT) if you want to make it official.
