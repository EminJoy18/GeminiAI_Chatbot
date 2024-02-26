import google.generativeai as genai

class GenAIException(Exception):
    '''base exception class that we are going to use to print the error message'''


class Chatbot:
    '''Chat can only have one candidate count'''
    CHATBOT_NAME = "My Gemini AI"

    # constructor
    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key = api_key)
        self.model = self.genai.GenerativeModel('gemini-pro')
        self.conversation = None
        self._conversation_history = []


        # to preload the conversation
        self.preload_conversation()



    def send_prompt(self, prompt, temperature = 0.1):
        if temperature < 0 or temperature > 1:
            raise GenAIException("Temperature must be between 0 and 1")
        
        if not prompt:
            raise GenAIException("Prompt cannot be empty")
        
        try:
            response = self.conversation.send_message(
                content = prompt,
                generation_config = self._generation_config(temperature),
            )
            response.resolve()
            
            return f'{response.text}\n' + '---' * 20
        
        except Exception as e:
            raise GenAIException(e.message)
        


    # to retrieve the conversation log
    # Using this GenerativeAI API, we can directly reference the history
    # can be done, by referencing the conversation object, then referencing the history object -> and that returns the conversation history
    # From each log its going to contain two keys, and its going to be an additional object
    # From each log, we can reference the row and text by referencing parts,
    # Since parts is going to return as a list, and with the CheckSessions Object -> we can have only one message at a time
    # So, we can refer 'message.text' to return the output
    # This is wrapped in a dictionary -> then compile all the conversation log into a list -> then return the list
    @property
    def history(self):
        conversation_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]



    # now in case we want to start a new conversation or want to reset the current existing seession
    def clear_conversation(self):
        self.conversation = self.model.start_chat(history = [])
        # clear the history list

    # method to initialise a conversation
    def start_conversation(self):
        self.conversation = self.model.start_chat(history = self._conversation_history)


    # we can change the configuration settings such as top end, top key, and the stop sequence settings - but now in this Chatbot app we only use the temperature 
    # 0 <= temperature <= 1
    # for a relatively creative response -> temperature = {0.8, 0.85, 0.9, 1.0}
    # for conservative response -> temperature = {0.8, 0.85, 0.9, 1.0}
    def _generation_config(self, temperature):
        return genai.types.GenerationConfig(
            temperature = temperature
        )


    # to simplify the message construction, another class is created
    def _construct_message(self, text, role = 'user'):
        return {
            'role': role,
            'parts': [text]
        }


    def preload_conversation(self, conversation_history = None):
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        
        else:
            self._conversation_history = [
                    self._construct_message('From now on, return the output as a JSON object that can be loaded in Python with the key as \'text\'. For example, {"text": "<output goes here>"}'), # default of Google is set to Markdown therefore we change t to JSON
                    self._construct_message('{"text": "Sure, I can return the output as a regular JSON object with the key as \'text\'. Here is an example: {"text": "Your Output"}.', 'model')
                ]