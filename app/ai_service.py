from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time
import requests
import logging

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MovieChatbot:
    def __init__(self):
        self.template = """You are a highly knowledgeable movie expert chatbot. Rules:
        - Answer in English only
        - Keep responses short and precise (1-2 sentences)
        - Use your extensive knowledge of:
          * Movies, directors, actors, genres
          * Film history and techniques
          * Box office data and awards
          * Movie trivia and behind-the-scenes facts
        - If unsure, say: "I'm not certain about that, but..."
        - Focus on accuracy over speculation
        - Cite years when mentioning movies

        Question: {question}
        Expert answer:"""

        logger.info("Initializing MovieChatbot...")
        
        try:
            # בדיקת זמינות השירות
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code != 200:
                logger.error(f"Ollama service check failed with status code: {response.status_code}")
                raise Exception("Ollama service is not available")
            logger.info("Ollama service is available")
            
            # יצירת המודל עם הגדרות מותאמות לתשובות חכמות ומדויקות יותר
            self.model = OllamaLLM(
                base_url="http://localhost:11434",
                model="mistral",
                temperature=0.3,  # יותר מדויק
                num_ctx=2048,     # הגדלת הקונטקסט לידע רחב יותר
                num_predict=150,  # מאפשר תשובות מעט ארוכות יותר כשצריך
                top_k=10,        # יותר אפשרויות לבחירת מילים
                top_p=0.3,       # פחות אקראיות
                repeat_penalty=1.2,
                num_thread=4,
                stop=["\n\n", "Question:", "Human:", "User:"]  # עצירה ברורה יותר
            )
            logger.info("Model initialized successfully")

            self.chain = (
                ChatPromptTemplate.from_template(self.template)
                | self.model
                | StrOutputParser()
            )
            logger.info("Chain created successfully")

        except Exception as e:
            logger.error(f"Error during initialization: {str(e)}")
            raise

    def get_response(self, user_input):
        try:
            logger.info(f"Received user input: {user_input}")

            current_time = time.strftime("%H:%M")  # פורמט 24 שעות

            if not user_input or not isinstance(user_input, str):
                logger.warning("Invalid input received")
                return {
                    "response": "I didn't catch that, try again!",
                    "time": current_time
                }

            # בדיקת זמינות השירות
            try:
                response = requests.get("http://localhost:11434/api/tags")
                if response.status_code != 200:
                    logger.error(f"Service check failed with status: {response.status_code}")
                    return {
                        "response": "Bot is on a coffee break, come back in a few minutes!",
                        "time": current_time
                    }
            except Exception as e:
                logger.error(f"Service check error: {str(e)}")
                return {
                    "response": "Bot is unavailable right now, try again soon!",
                    "time": current_time
                }

            logger.info("Sending request to model")
            result = self.chain.invoke({
                "question": user_input
            })
            logger.info(f"Received response from model: {result}")

            if not result or len(result.strip()) == 0:
                logger.warning("Empty response received from model")
                return {
                    "response": "I didn't understand that, try rephrasing!",
                    "time": current_time
                }

            return {
                "response": result.strip(),
                "time": current_time
            }

        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}", exc_info=True)
            return {
                "response": "Oops! Something went wrong, try again in a moment!",
                "time": time.strftime("%H:%M")
            }
