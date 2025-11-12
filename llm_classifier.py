import os
import logging
from typing import Dict, Tuple
from llama_index.llms.openai import OpenAI
from config import PYDANTIC_CLASSIFICATION_PROMPT , API_CONFIG
from format_llm_response import parse_llm_response
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClassifier:
    """
    LLM-based document classifier using GPT-4o-mini.
    Supports both image and text input.
    """
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize LLM classifier.
        
        Args:
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
            model: Model name (default: gpt-4o-mini)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.model = model or API_CONFIG["model"]
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize OpenAI LLM."""
        try:
            self.llm = OpenAI(
                model=self.model,
                api_key=self.api_key,
                temperature=API_CONFIG.get("temperature", 0.2),
                max_tokens=API_CONFIG.get("max_tokens", 1000)
            )
            logger.info(f"LLM initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise

    def classify_text(self, text: str):
        """
        Classify a document based on extracted text.
        
        Args:
            text: Extracted document text
            
        Returns:
            Tuple of (classification_dict, processing_time_ms)
        """
        if not text or not text.strip():
            raise ValueError("Text content is empty")
        
        try:            
            # Prepare prompt with text content
            prompt = PYDANTIC_CLASSIFICATION_PROMPT.format(context_str=text)
            response = self.llm.complete(prompt)
            formatted_response = parse_llm_response(llm_response=str(response))
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error classifying text: {str(e)}")
            raise
