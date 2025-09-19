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
        self.conversation_history = []
        self.template = """You are a movie expert chatbot. Rules:
        - Answer in English only
        - IMPORTANT: Answer super fast. less than 5 seconds to respond!
        - Keep responses short (2-3 sentences maximum)
        - Be direct and to the point
        - Use your knowledge of movies, directors, actors
        - If unsure, say: "I'm not certain"
        - Cite years for movies
        - Add relevant emojis to your responses (1-2 emojis maximum)
        - Start each response with an appropriate emoji

        Previous conversation:
        {history}

        Question: {question}
        Expert answer:"""

        logger.info("Initializing MovieChatbot...")
        
        try:
            # Service availability check
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code != 200:
                logger.error(f"Ollama service check failed with status code: {response.status_code}")
                raise Exception("Ollama service is not available")
            logger.info("Ollama service is available")
            
            # Optimized model settings for maximum speed
            self.model = OllamaLLM(
                base_url="http://localhost:11434",
                model="mistral",
                temperature=0.1,
                num_ctx=512,      
                num_predict=100,  
                top_k=3,         
                top_p=0.1,       
                repeat_penalty=1.1,
                num_thread=8,    
                stop=["Question:", "Human:", "User:"]
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

            if not user_input or not isinstance(user_input, str):
                logger.warning("Invalid input received")
                return {
                    "response": "❓ I didn't catch that, try again!",
                    "time": time.strftime("%H:%M")
                }

            # הכנת היסטוריית השיחה
            history = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.conversation_history[-3:]])  # שמירת 3 הודעות אחרונות
            
            # Service availability check
            try:
                response = requests.get("http://localhost:11434/api/tags")
                if response.status_code != 200:
                    logger.error(f"Service check failed with status: {response.status_code}")
                    return {
                        "response": "☕ Bot is on a coffee break, come back in a few minutes!",
                        "time": time.strftime("%H:%M")
                    }
            except Exception as e:
                logger.error(f"Service check error: {str(e)}")
                return {
                    "response": "🔧 Bot is unavailable right now, try again soon!",
                    "time": time.strftime("%H:%M")
                }

            logger.info("Sending request to model")
            result = self.chain.invoke({
                "question": user_input,
                "history": history
            })
            
            # שמירת השיחה הנוכחית
            self.conversation_history.append((user_input, result.strip()))
            
            logger.info(f"Received response from model: {result}")

            # Set timestamp at response time
            response_time = time.strftime("%H:%M")

            if not result or len(result.strip()) == 0:
                logger.warning("Empty response received from model")
                return {
                    "response": "🤔 I didn't understand that, try rephrasing!",
                    "time": response_time
                }

            return {
                "response": result.strip(),
                "time": response_time
            }

        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}", exc_info=True)
            return {
                "response": "⚠️ Oops! Something went wrong, try again in a moment!",
                "time": time.strftime("%H:%M")
            }
