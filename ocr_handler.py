"""
OCR Handler for extracting text from images.
Uses EasyOCR for robust text extraction.
"""

import easyocr
import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRHandler:
    """
    Handles OCR operations for document images.
    Extracts text from images using EasyOCR.
    """
    
    def __init__(self, languages: list = None, gpu: bool = False):
        """
        Initialize OCR handler.
        
        Args:
            languages: List of language codes (default: ['en'])
            gpu: Whether to use GPU (default: False)
        """
        self.languages = languages or ['en']
        self.gpu = gpu
        self.reader = None
        self._initialize_reader()
    
    def _initialize_reader(self):
        """Initialize EasyOCR reader."""
        try:
            self.reader = easyocr.Reader(
                self.languages,
                gpu=self.gpu,
                verbose=False
            )
            logger.info(f"OCR reader initialized with languages: {self.languages}")
        except Exception as e:
            logger.error(f"Failed to initialize OCR reader: {str(e)}")
            raise
    
    def extract_text_from_image(self, image_path: str) -> Tuple[str, float]:
        """
        Extract text from an image file.
        
        Steps :
            1. Read image
            2. Extract text using EasyOCR
            3. Calculate average confidence
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            # Read image
            image = cv2.imread(str(image_path))
            if image is None:
                raise ValueError(f"Failed to read image: {image_path}")
            
            # Extract text using EasyOCR
            results = self.reader.readtext(image, detail=1)
            
            if not results:
                logger.warning(f"No text extracted from image: {image_path}")
                return "", 0.0
            
            # Combine text and calculate average confidence
            extracted_text = "\n".join([text[1] for text in results])
            avg_confidence = np.mean([text[2] for text in results])
            
            logger.info(f"Extracted text from {image_path} with confidence: {avg_confidence:.2f}")
            return extracted_text, float(avg_confidence)
            
        except Exception as e:
            logger.error(f"Error extracting text from {image_path}: {str(e)}")
            raise

