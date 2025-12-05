EPICS Project: AI-Based Drone Surveillance System for Wildlife Protection

Overview
This project is a multi-drone surveillance system designed for wildlife protection. It leverages Artificial Intelligence  to detect animals, humans (potential poachers), and threats like forest fires from drone imagery. The system aims to provide real-time alerts and a coordination platform for forest rangers.

Features
- Object Detection: Identifies wildlife, humans, and various types of threats using trained YOLOv8 models.
- Multi-Drone Coordination: (Planned) Manages a fleet of drones for broad area coverage.
- Web Dashboard: (Planned) Visual interface for monitoring drone feeds and alerts.
- Backend API: RESTful API built with FastAPI to handle data processing and user management.

Project Structure
The repository is organized as follows:

- Directory: AIML - Contains the core AI logic and dataset tools.
  - Models: Directory for storing trained model weights.
  - Datasets: Raw and processed datasets for training.
  - PythonCodes: Scripts for dataset manipulation and training
- Directory: BackEnd - The server-side application.
  -main.py: Entry point for the FastAPI application.
  - *(Note: The backend seems to expect an app package structure which is currently being set up).*
- Directory: FrontEnd - (In Development) Source code for the web dashboard.
- Directory: DroneFiles - Configuration and flight control scripts for physical drones.
- Directory: Documentation - Project documentation files.

Getting Started

Prerequisites
- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Ultralytics YOLO](https://docs.ultralytics.com/) (for AI module)
- Matplotlib, NumPy (for data visualization)

AI Module Setup
1. Navigate to the 'AIML/PythonCodes' directory.
2. Ensure your dataset is configured in data.yaml.
3. Use utilities (the python codes provided) to prepare your dataset splits (train/val/test).

 Backend Setup
1. Navigate to the 'BackEnd' directory.
2. Install dependencies (create a `requirements.txt` if needed, but generally: `pip install fastapi ultralytics sqlalchemy`).
3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```
   *(Note: Ensure the proper python package structure for `app` is in place).*

## Documentation
For a deep dive into the system architecture and theoretical background, refer to the files in the `Documentation` folder:
- `Forest Surveillance Using Drone.pdf`
- `Forest Surveillance Using Drone.docx`
