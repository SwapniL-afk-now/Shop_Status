import torch
from transformers import OwlViTProcessor, OwlViTForObjectDetection
from PIL import Image
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class ShopStatusDetector:
    def __init__(self, model_name: str = "google/owlvit-base-patch32"):
        self.model_name = model_name
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """Loads the OwlViT model and processor."""
        logger.info(f"Loading OwlViT model '{self.model_name}' on {self.device}...")
        try:
            self.processor = OwlViTProcessor.from_pretrained(self.model_name)
            self.model = OwlViTForObjectDetection.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def classify(self, image: Image.Image) -> Dict[str, any]:
        """
        Classifies whether a shop is open or closed based on the image.
        Uses OwlViT for zero-shot object detection with specific text queries.
        """
        if not self.processor or not self.model:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        try:
            # Define descriptive queries for OwlViT
            text_queries = [
                "an open shop entrance with visible interior",
                "a closed shop with metal shutter pulled down",
                "shop door open",
                "shop shutter closed",
                "store entrance open",
                "rolling shutter down"
            ]
            
            image = image.convert("RGB")
            inputs = self.processor(text=[text_queries], images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Post-process to get all detections (threshold=0.0 to find best match even if low confidence)
            target_sizes = torch.Tensor([image.size[::-1]]).to(self.device)
            results = self.processor.post_process_object_detection(
                outputs=outputs,
                threshold=0.0,
                target_sizes=target_sizes
            )

            scores = results[0]["scores"]
            labels = results[0]["labels"]

            if len(scores) == 0:
                return {
                    "status": "open",
                    "message": "Shop is Open (default - no strong indicators)",
                    "confidence": 0.5,
                    "detected_label": "none"
                }

            # Pick the best detection
            best_idx = scores.argmax()
            best_score = scores[best_idx].item()
            best_label = text_queries[labels[best_idx].item()]

            # Determine status
            closed_keywords = ["closed", "shutter", "down", "pulled down"]
            open_keywords = ["open", "entrance", "visible", "door"]
            
            label_lower = best_label.lower()
            has_closed = any(kw in label_lower for kw in closed_keywords)
            has_open = any(kw in label_lower for kw in open_keywords)

            if has_closed and not has_open:
                status, message = "closed", "Shop is Closed"
            else:
                status, message = "open", "Shop is Open"

            return {
                "status": status,
                "message": message,
                "confidence": round(float(max(best_score, 0.01)), 4),
                "detected_label": best_label
            }

        except Exception as e:
            logger.error(f"Classification error: {e}", exc_info=True)
            return {
                "status": "unknown",
                "message": f"Error: {str(e)}",
                "confidence": 0.0,
                "detected_label": "error"
            }
