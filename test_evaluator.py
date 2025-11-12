"""
Small-scale test for AccuracyMetric (10 images only).

This script tests the accuracy metric on a small subset to verify:
1. Data preparation works
2. Classifier runs without errors
3. Accuracy calculation is correct
4. Results are as expected

After verifying this works, run test_accuracy_metric.py for full evaluation.
"""

import logging
import os
from pathlib import Path
from classifier import DocumentClassifier
from evaluator import AccuracyMetric
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main_small_test():
    """
    Run accuracy evaluation on 10 test images only.

    Steps : 
        Step 1: Initialize classifier.
        Step 2: Initialize AccuracyMetric.
        Step 3: Prepare test dataset.
        Step 4: Take only first 10 images from test set
        Step 5: Evaluate on small test set
    """
    logger.info("\nStep 1: Initializing DocumentClassifier...")
    api_key = os.getenv("OPENAI_API_KEY")
    classifier = DocumentClassifier(api_key=api_key, ocr_gpu=False)
    logger.info("Step 2: Initializing AccuracyMetric...")
    metric = AccuracyMetric(random_seed=42)
    logger.info("Step 3: Preparing test dataset (80/20 split)...")
    base_path = Path(__file__).parent  # Parent directory containing all folders
    test_set = metric.prepare_test_dataset(base_path, test_percentage=0.2)
    logger.info(f"\nStep 4: Selecting first 10 images from test set...")
    small_test_set = test_set[:10]
    logger.info(f"Small test set size: {len(small_test_set)}")
    
    logger.info("\nImages to test:")
    for idx, (image_path, true_label) in enumerate(small_test_set, 1):
        logger.info(f"  {idx}. {Path(image_path).name} → {true_label}")
    

    logger.info("\nStep 5: Running evaluation on 10 test images...")
    results = metric.evaluate(classifier, small_test_set)
    return results



if __name__ == "__main__":
    results = main_small_test()
    
