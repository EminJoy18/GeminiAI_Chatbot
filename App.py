from configparser import ConfigParser
from Chatbot import Chatbot
import sys

def main():
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = config['gemini_ai']['API_KEY']

    chatbot = Chatbot(api_key = api_key)
    chatbot.start_conversation()
    #chatbot.clear_conversation()

    print("Welcome to the JJ Gemini Chatbot CLI. Type 'quit' to exit.")

    # print('{0}: {1}'.format(chatbot.CHATBOT_NAME, chatbot.history[-1]['text']))
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            sys.exit("Exiting Chatbot CLI...")
            # print("Exiting Chatbot CLI...")
            # break

        try:
            response = chatbot.send_prompt(user_input)
            print(f"{chatbot.CHATBOT_NAME}: {response[10:-2]}") # because is a response string, not dictionary
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()  # calling the main function