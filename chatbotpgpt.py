
import os
import dotenv
from openai import OpenAI
from openai import APIError, APIConnectionError, RateLimitError


# ============================================================
# 1. ENVIRONMENT CONFIGURATION
# ============================================================

# Load environment variables from the .env file.
dotenv.load_dotenv()

# Retrieve the Groq API key.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Stop the program if the API key is missing.
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")


# ============================================================
# 2. INITIALIZE THE AI CLIENT
# ============================================================

# Create an OpenAI-compatible client using Groq.
llm = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Specify the AI model.
MODEL = "openai/gpt-oss-120b"


# ============================================================
# 3. CONVERSATION HISTORY
# ============================================================

# Store system instructions and conversation history.
messages = [
    {
        "role": "system",
        "content": (
           "You are a helpful assistant. "
        )
    }
]


# ============================================================
# 4. TOKEN TRACKING VARIABLES
# ============================================================

# Track cumulative token consumption throughout the session.
total_prompt_tokens = 0
total_completion_tokens = 0
total_tokens = 0

# Track the number of successful API requests.
total_requests = 0


# ============================================================
# 5. CHATBOT FUNCTION
# ============================================================

def bot(message):
    """
    Sends the user's message to the AI model.

    Functions:
    - Adds the user's message to conversation history.
    - Sends the conversation to Groq.
    - Retrieves the AI-generated response.
    - Tracks token consumption.
    - Saves the AI response in conversation history.

    Returns:
        tuple: AI-generated response and token usage.
    """

    global total_prompt_tokens
    global total_completion_tokens
    global total_tokens
    global total_requests

    # Add the user's message to conversation history.
    messages.append({
        "role": "user",
        "content": message
    })

    try:
        # Send conversation history to the AI model.
        response = llm.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        # Extract token usage from the API response.
        usage = response.usage

        if usage is not None:
            prompt_tokens = usage.prompt_tokens or 0
            completion_tokens = usage.completion_tokens or 0
            consumed_tokens = usage.total_tokens or 0

        else:
            # Usage information may not be available.
            prompt_tokens = 0
            completion_tokens = 0
            consumed_tokens = 0

        # Update cumulative session token consumption.
        total_prompt_tokens += prompt_tokens
        total_completion_tokens += completion_tokens
        total_tokens += consumed_tokens

        # Retrieve the AI-generated response.
        response_text = response.choices[0].message.content

        # Provide a fallback if the AI returns an empty response.
        if not response_text:
            response_text = "Sorry, I could not generate a response."

        # Save the AI response in conversation history.
        messages.append({
            "role": "assistant",
            "content": response_text
        })

        # Count successful API requests.
        total_requests += 1

        # Store current request token consumption.
        token_usage = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": consumed_tokens
        }

        # Return both the AI response and token information.
        return response_text, token_usage

    except RateLimitError:
        messages.pop()
        return "API rate limit reached. Please try again later.", None

    except APIConnectionError:
        messages.pop()
        return "Connection error. Please check your internet connection.", None

    except APIError as error:
        messages.pop()
        return f"API error: {error}", None

    except Exception as error:
        messages.pop()
        return f"Unexpected error: {error}", None


# ============================================================
# 6. DISPLAY TOKEN USAGE
# ============================================================

def display_token_usage(usage):
    """
    Displays token consumption for the current API request.

    Parameters:
        usage (dict): Token consumption information.
    """

    if usage is None:
        return

    print("\n" + "=" * 40)
    print("TOKEN USAGE - CURRENT REQUEST")
    print("=" * 40)

    print(f"Prompt Tokens     : {usage['prompt_tokens']}")
    print(f"Completion Tokens : {usage['completion_tokens']}")
    print(f"Total Tokens      : {usage['total_tokens']}")

    print("=" * 40)


# ============================================================
# 7. DISPLAY SESSION SUMMARY
# ============================================================

def display_summary():
    """
    Displays cumulative token consumption after the chatbot exits.
    """

    print("\n" + "=" * 40)
    print("CHAT SESSION SUMMARY")
    print("=" * 40)

    print(f"Total API Requests       : {total_requests}")
    print(f"Total Prompt Tokens      : {total_prompt_tokens}")
    print(f"Total Completion Tokens  : {total_completion_tokens}")
    print(f"Total Tokens Consumed    : {total_tokens}")

    print("=" * 40)


# ============================================================
# 8. CHAT FUNCTION
# ============================================================

def chat():
    """
    Runs the chatbot interaction loop.

    Continues accepting user input until the user types
    'quit' or 'exit'.
    """

    print("\nAI CHATBOT")
    print("Type 'quit' or 'exit' to terminate the conversation.")
    print("-" * 40)

    greeting = "Hi! I'm your AI assistant. How can I help you today?"
    print(f"\nBot: {greeting}")
    messages.append({"role": "assistant", "content": greeting})
    
    while True:

        # Get input from the user.
        user_input = input("\nAsk Something: ").strip()

        # Check whether the user wants to exit.
        if user_input.lower() in ["quit", "exit"]:
            print("\nExiting the chatbot. Goodbye!")
            break

        # Prevent empty messages from being sent to the API.
        if not user_input:
            print("Please enter a message.")
            continue

        # Send the message to the AI.
        bot_answer, usage = bot(user_input)

        # Display the AI response FIRST.
        print(f"\nBot: {bot_answer}")

        # Display token consumption AFTER the AI response.
        display_token_usage(usage)


# ============================================================
# 9. MAIN FUNCTION
# ============================================================

def main():
    """
    Main entry point of the application.

    Starts the chatbot and displays the session summary
    after the conversation ends.
    """

    try:
        chat()

    except KeyboardInterrupt:
        # Allow the user to terminate using CTRL + C.
        print("\n\nChatbot interrupted by user.")

    finally:
        # Always display the session summary.
        display_summary()


# ============================================================
# 10. EXECUTE THE APPLICATION
# ============================================================

# Run main() only when this file is executed directly.
if __name__ == "__main__":
    main()
