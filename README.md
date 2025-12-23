# Shop Status Detector

A professional, modularized vision-based application that detects whether a shop is open or closed using the **OwlViT (Vision Transformer)** model for zero-shot object detection.

## 🚀 Features

- **Zero-Shot Detection**: Uses Google's OwlViT model to detect visual features of open/closed shops without specific training.
- **RESTful API**: Fast and robust API built with FastAPI.
- **Premium UI**: Modern, glassmorphic frontend for seamless user experience.
- **Modular Design**: Separated concerns for ML logic, API, and frontend.

## 📂 Project Structure

```text
├── src/
│   ├── detector.py      # Core ML logic (Model loading & classification)
│   └── api.py           # FastAPI routes and middleware
├── public/
│   └── index.html       # High-fidelity web frontend
├── main.py              # Entry point to run the server
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```

## 🛠️ Installation

1. **Clone the repository** (or navigate to the directory).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Usage

Start the server using `main.py`:

```bash
python main.py
```

The application will be available at `http://localhost:8000`.

### API Endpoints

- **GET `/api/health`**: Check service and model status.
- **POST `/api/detect-status`**: Upload an image to get shop status detection.
  - Parameters: `file` (Image)
  - Returns: `{"status": "open|closed", "message": "...", "confidence": 0.XX, "detected_label": "..."}`

## 🧠 Technical Details

The system uses **OwlViT**, a zero-shot text-conditioned object detector. Instead of manual feature engineering, it searches for visual cues like:
- "open shop entrance with visible interior"
- "closed shop with metal shutter pulled down"
- "rolling shutter down"

This approach allows high flexibility and handles various shop types without retraining.
