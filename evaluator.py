import logging
import random
from pathlib import Path
from typing import List, Tuple, Dict
from sklearn.metrics import accuracy_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AccuracyMetric:
    """
    Evaluates document classifier accuracy on a test dataset.
    
    Workflow:
    1. prepare_test_dataset() - Scans folders, creates 80/20 split
    2. evaluate() - Runs classifier on test set, calculates accuracy
    3. get_confusion_matrix() - Analyzes misclassifications
    """
    
    def __init__(self, random_seed: int = 42):
        """
        Initialize AccuracyMetric.
        
        Args:
            random_seed: For reproducible 80/20 split (default: 42)
        """
        self.random_seed = random_seed
        random.seed(random_seed)
        self.categories = ["Bank Statement", "Check", "ITR_Form 16", "Salary Slip", "Utility"]
        logger.info(f"AccuracyMetric initialized with random_seed={random_seed}")
    
    def prepare_test_dataset(self, base_path: str, test_percentage: float = 0.2) -> List[Tuple[str, str]]:
        """
        Scan all document folders and create 80/20 train-test split.
        
        Args:
            base_path: Path to parent directory containing document folders
            test_percentage: Percentage for test set (default: 0.2 = 20%)
        
        Returns:
            test_set: List of (image_path, true_label) tuples for test set
        
        """
        base_path = Path(base_path)
        
        if not base_path.exists():
            raise FileNotFoundError(f"Base path not found: {base_path}")
        
        logger.info(f"Scanning folders in: {base_path}")
        
        # Define document categories (folder names)
        categories = ["Bank Statement", "Check", "ITR_Form 16", "Salary Slip", "Utility"]
        
        all_images = []
        
        # Scan each category folder
        for category in categories:
            category_path = base_path / category
            
            if not category_path.exists():
                logger.warning(f"Category folder not found: {category_path}")
                continue
            
            # Get all .jpg files in this category
            jpg_files = list(category_path.glob("*.jpg"))
            logger.info(f"Found {len(jpg_files)} images in {category}")
            
            # Create (image_path, true_label) tuples
            for image_path in jpg_files:
                all_images.append((str(image_path), category))
        
        logger.info(f"Total images found: {len(all_images)}")
        
        # Shuffle and split 80/20
        random.shuffle(all_images)
        split_index = int(len(all_images) * (1 - test_percentage))
        
        train_set = all_images[:split_index]
        test_set = all_images[split_index:]
        
        logger.info(f"Train set size: {len(train_set)} ({100*(1-test_percentage):.0f}%)")
        logger.info(f"Test set size: {len(test_set)} ({100*test_percentage:.0f}%)")
        
        # Log test set distribution
        test_distribution = {}
        for _, label in test_set:
            test_distribution[label] = test_distribution.get(label, 0) + 1
        
        logger.info("Test set distribution:")
        for label, count in sorted(test_distribution.items()):
            logger.info(f"  {label}: {count}")
        
        return test_set
    
    def evaluate(self, classifier, test_set: List[Tuple[str, str]]) -> Dict:
        """
        Run classifier on test set and calculate accuracy.
        
        Args:
            classifier: DocumentClassifier instance with classify_image() method
            test_set: List of (image_path, true_label) tuples
        
        Returns:
            results: Dictionary with:
                - accuracy: Overall accuracy (0.0 to 1.0)
                - correct_predictions: Number of correct predictions
                - total_predictions: Total number of predictions
                - incorrect_predictions: Number of incorrect predictions
                - y_true: List of true labels
                - y_pred: List of predicted labels
        
        """
        logger.info(f"Starting evaluation on {len(test_set)} test images...")
        
        y_true = []
        y_pred = []
        errors = []
        
        for idx, (image_path, true_label) in enumerate(test_set, 1):
            try:
                # Run classifier
                prediction = classifier.classify_image(image_path)
                print("Prediction Output",prediction)
                predicted_label = prediction.get("document_type", "unknown")
                
                y_true.append(true_label)
                y_pred.append(predicted_label)
                
                # Log progress every 10 images
                if idx % 10 == 0:
                    logger.info(f"Processed {idx}/{len(test_set)} images")
                
            except Exception as e:
                # Error handling: Count as incorrect prediction
                logger.warning(f"Error processing {image_path}: {str(e)}")
                y_true.append(true_label)
                y_pred.append("unknown")  # Treat error as "unknown" prediction
                errors.append({
                    "image_path": image_path,
                    "true_label": true_label,
                    "error": str(e)
                })
        
        # Calculate accuracy using scikit-learn
        accuracy = accuracy_score(y_true, y_pred)
        print("Accuracy", accuracy)
        correct_predictions = sum(1 for t, p in zip(y_true, y_pred) if t == p)
        total_predictions = len(y_true)
        incorrect_predictions = total_predictions - correct_predictions
        
        results = {
            "accuracy": accuracy,
            "correct_predictions": correct_predictions,
            "total_predictions": total_predictions,
            "incorrect_predictions": incorrect_predictions,
            "y_true": y_true,
            "y_pred": y_pred,
            "errors": errors
        }
        
        # Log results
        logger.info("=" * 60)
        logger.info("ACCURACY EVALUATION RESULTS")
        logger.info("=" * 60)
        logger.info(f"Accuracy: {accuracy:.2%}")
        logger.info(f"Correct Predictions: {correct_predictions}/{total_predictions}")
        logger.info(f"Incorrect Predictions: {incorrect_predictions}")
        
        if errors:
            logger.warning(f"Errors encountered: {len(errors)}")
            for error in errors[:5]:  # Show first 5 errors
                logger.warning(f"  {error['image_path']}: {error['error']}")
        
        logger.info("=" * 60)
        
        return results
