import os
from classifier import DocumentClassifier
from ocr_handler import OCRHandler

from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the unified classifier
api_key = os.getenv("OPENAI_API_KEY")

classifier = DocumentClassifier(api_key=api_key, ocr_gpu=False)

ocr_handler = OCRHandler(languages=['en'], gpu=False)

#image_file_path = "./Bank Statement/82.jpg"

# Check Statements :
#image_file_path = "./Check/59.jpg"

# ITR Forms 16 :
#image_file_path = "./ITR_FORM 16/14.jpg"

# Salary Slip :
image_file_path = "./Salary Slip/102.jpg"

# Utility : 
#image_file_path = "./Utility/66.jpg"

## Testing for the Text directly ..
text, score = ocr_handler.extract_text_from_image(image_path=image_file_path)
#print("Text:", text)

response = classifier.extract_schema_from_text(ocr_text=text)
print("Response",response)