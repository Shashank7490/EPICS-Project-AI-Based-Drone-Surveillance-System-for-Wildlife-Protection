# Forest Surveillance Backend

FastAPI backend for the Multi-Drone AI-Based Wildlife Surveillance System.

## What this backend does
- Receives detection data from the YOLOv8 model
- Serves detection data to the frontend dashboard
- Handles drone commands (takeoff, land, move, return)
- Manages alerts when threats are detected
- Connects to AirSim simulation (simulation mode by default)

## Setup

1. Create virtual environment
python -m venv venv

2. Activate it
Windows: venv\Scripts\activate

3. Install dependencies
pip install "fastapi[standard]" uvicorn pydantic

4. Run the server
uvicorn app.main:app --reload

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| POST | /detections | Receive detection from model |
| GET | /detections | Get all detections |
| GET | /detections/{drone_id} | Get detections by drone |
| DELETE | /detections | Clear all detections |
| POST | /drone/takeoff | Takeoff command |
| POST | /drone/land | Land command |
| POST | /drone/move | Move to location |
| POST | /drone/return | Return to base |
| GET | /drone/status/{drone_id} | Get drone status |
| POST | /alerts | Create alert |
| GET | /alerts | Get all alerts |
| GET | /alerts/active | Get active alerts |
| PUT | /alerts/{alert_id}/resolve | Resolve an alert |

## To enable real AirSim connection
In `app/airsim_bridge.py`, change:
AIRSIM_ENABLED = False
to:
AIRSIM_ENABLED = True
