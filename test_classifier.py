import os
from classifier import DocumentClassifier
from ocr_handler import OCRHandler

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
classifier = DocumentClassifier(api_key=api_key, ocr_gpu=False)
ocr_handler = OCRHandler(languages=['en'], gpu=False)


def test_image_classification(image_file_path: str):
    """Test classification directly from image file."""
    result = classifier.classify_image(image_file_path)
    print("Classification Result:\n", result)


def test_text_classification(image_file_path: str):
    """Test classification from OCR text extracted from image."""
    # Extract text from image
    text, score = ocr_handler.extract_text_from_image(image_path=image_file_path)
    print("Classification Result for extracting text from the image:\n", text)



if __name__ == "__main__":
    # Test image paths
    image_file_path = "./Bank Statement/82.jpg"
    # image_file_path = "./Salary Slip/102.jpg"
    
    # Run tests - comment/uncomment as needed
    test_image_classification(image_file_path)
    #test_text_classification(image_file_path)