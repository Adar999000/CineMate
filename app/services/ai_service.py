import os
import time
import logging
import requests
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

        # אם אין OLLAMA_BASE_URL בסביבה — אל תאתחל את הבוט (כדי לא להפיל את השרת ב-Render)
        base_url = os.getenv("OLLAMA_BASE_URL")
        if not base_url:
            logger.warning("MovieChatbot disabled: OLLAMA_BASE_URL not set. Skipping Ollama initialization.")
            self.enabled = False
            self.chain = None
            return

        base_url = base_url.rstrip("/")
        model_name = os.getenv("OLLAMA_MODEL", "mistral")

        try:
            # בדיקת זמינות השרת החיצוני של Ollama
            r = requests.get(f"{base_url}/api/tags", timeout=3)
            r.raise_for_status()
            logger.info("Ollama service is available at %s", base_url)

            # מודל Ollama עם פרמטרים ניתנים להגדרה דרך ENV
            self.model = OllamaLLM(
                base_url=base_url,
                model=model_name,
                temperature=float(os.getenv("OLLAMA_TEMPERATURE", "0.1")),
                num_ctx=int(os.getenv("OLLAMA_NUM_CTX", "512")),
                num_predict=int(os.getenv("OLLAMA_NUM_PREDICT", "100")),
                top_k=int(os.getenv("OLLAMA_TOP_K", "3")),
                top_p=float(os.getenv("OLLAMA_TOP_P", "0.1")),
                repeat_penalty=float(os.getenv("OLLAMA_REPEAT_PENALTY", "1.1")),
                stop=["Question:", "Human:", "User:"],
            )

            self.chain = (
                ChatPromptTemplate.from_template(self.template)
                | self.model
                | StrOutputParser()
            )
            self.enabled = True
            logger.info("Model & chain initialized successfully")

        except Exception as e:
            logger.error("MovieChatbot init failed to reach Ollama at %s: %s", base_url, e)
            # כבה את הבוט אבל אל תפיל את השרת
            self.enabled = False
            self.chain = None

    def get_response(self, user_input):
        try:
            logger.info("Received user input: %s", user_input)

            if not user_input or not isinstance(user_input, str) or not user_input.strip():
                logger.warning("Invalid input received")
                return {
                    "response": "❓ I didn't catch that, try again!",
                    "time": time.strftime("%H:%M")
                }

            # אם הבוט מכובה (למשל אין OLLAMA_BASE_URL) — החזר הודעה ידידותית
            if not getattr(self, "enabled", False) or not self.chain:
                return {
                    "response": "🤖 The chatbot is temporarily unavailable here. Try again later!",
                    "time": time.strftime("%H:%M")
                }

            # היסטוריית שיחה קצרה (3 אחרונות)
            history = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.conversation_history[-3:]])

            logger.info("Sending request to model")
            result = self.chain.invoke({
                "question": user_input.strip(),
                "history": history
            })

            cleaned = (result or "").strip()
            self.conversation_history.append((user_input, cleaned))

            response_time = time.strftime("%H:%M")
            if not cleaned:
                logger.warning("Empty response received from model")
                return {
                    "response": "🤔 I didn't understand that, try rephrasing!",
                    "time": response_time
                }

            return {
                "response": cleaned,
                "time": response_time
            }

        except Exception as e:
            logger.error("Error in get_response: %s", e, exc_info=True)
            return {
                "response": "⚠️ Oops! Something went wrong, try again in a moment!",
                "time": time.strftime("%H:%M")
            }
