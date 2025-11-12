import logging
from typing import Dict
from pathlib import Path
from llm_classifier import LLMClassifier
from ocr_handler import OCRHandler
from extraction_schema import DocumentExtraction
from llama_index.core.program import LLMTextCompletionProgram
from ocr_handler import OCRHandler
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentClassifier:
    """
    Main document classifier that handles both image and text input.
    Orchestrates OCR, LLM classification, and confidence scoring.
    """
    
    def __init__(self, api_key: str = None, ocr_gpu: bool = False):
        """
        Initialize the unified document classifier.
        
        Args:
            api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)
            ocr_gpu: Whether to use GPU for OCR (default: False)
        """
        self.llm_classifier = LLMClassifier(api_key=api_key)
        self.ocr_handler = OCRHandler(languages=['en'], gpu=ocr_gpu)
        logger.info("DocumentClassifier initialized with OCR and LLM components")
    
    def classify_image(self, image_path: str) -> Dict:
        """
        Classify a document from an image file.
        Orchestrates OCR extraction and LLM classification.
        
        Steps :
            1. Extract text from image using OCR
            2. Classify the extracted text using LLM
            3. Parse LLM response
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            logger.info(f"Starting classification pipeline for: {image_path}")
            logger.info("Step 1: Extracting text from image using OCR")
            extracted_text, ocr_confidence = self.ocr_handler.extract_text_from_image(
                image_path=str(image_path)
            )
            
            if not extracted_text or not extracted_text.strip():
                logger.warning(f"No text extracted from image: {image_path}")
                return {
                    "document_type": "unknown",
                    "confidence": 0.0,
                    "reasoning": "No text could be extracted from the image",
                    "key_indicators": [],
                    "negative_indicators": [],
                    "ocr_confidence": ocr_confidence,
                    "combined_confidence": 0.0,
                    "error": "Empty OCR result"
                }
            
            logger.info(f"OCR extraction successful. Confidence: {ocr_confidence:.2f}")
            logger.info("Step 2: Classifying extracted text using LLM")
            llm_response = self.llm_classifier.classify_text(text=extracted_text)
            logger.info("Step 3: Parsing LLM response")
            return llm_response
            
        except Exception as e:
            logger.error(f"Error in classification pipeline: {str(e)}")
            raise
    
    def classify_text(self, text: str) -> Dict:
        """
        Classify a document based on text content directly.
        Bypasses OCR extraction.
        
        Steps :
            1. Parse text into the LLM
        """
        if not text or not text.strip():
            raise ValueError("Text content is empty")
        
        try:
            logger.info("Starting text-based classification (no OCR)")
            
            if not text or not text.strip():
                logger.warning(f"No text extracted.")
                return {
                    "document_type": "unknown",
                    "confidence": 0.0,
                    "reasoning": "No text could be extracted from the image",
                    "key_indicators": [],
                    "negative_indicators": [],
                    "combined_confidence": 0.0,
                    "error": "Empty OCR result"
                }            
            # Classify using LLM
            llm_response = self.llm_classifier.classify_text(text=text)
            
            logger.info("Text classification complete:")
            
            return llm_response
            
        except Exception as e:
            logger.error(f"Error in text classification: {str(e)}")
            raise

    def extract_schema_from_text(self, ocr_text: str) -> DocumentExtraction:
        """
        Convert OCR text to structured data using LLM
        """
        prompt_template = f"""
        You are extracting information from a OCR Text:
        {ocr_text}
        
        Extract the following fields and return as JSON:
        - For bank_statement: account_holder_name, account_number, statement_period_start, etc.
        - For salary_slip: employee_name, employee_id, month, year, basic_salary, etc.
        - For itr: taxpayer_name, pan_number, assessment_year, total_income, tax_payable, filing_date
        - For utility_bill: consumer_name, consumer_number, bill_date, due_date, etc.
        - For check: check_number, date, payee_name, amount_in_numbers, amount_in_words, etc.
        
        Set confidence (0.0-1.0) based on how clear the text is.
        """
        
        program = LLMTextCompletionProgram.from_defaults(
            output_cls=DocumentExtraction,
            prompt_template_str=prompt_template,
            verbose=True
        )
        
        result = program(ocr_text=ocr_text)
        return result

