import os
import time
import logging

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MovieChatbot:
    def __init__(self):
        # Ollama is disabled for cloud deployment
        self.llm = None
        
    def get_response(self, user_input, movies_context=""):
        # Fallback response when Ollama is not available
        return "מצטער, שירות הצ'אטבוט אינו זמין כרגע. אנא נסה שוב מאוחר יותר."
