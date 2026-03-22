from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from app.airsim_bridge import airsim_takeoff, airsim_land, airsim_move, airsim_return

router = APIRouter()

class Detection(BaseModel):
    drone_id: str
    class_name: str
    confidence: float
    x1: int
    y1: int
    x2: int     
    y2: int

class DroneCommand(BaseModel):
    drone_id: str
    x: float = 0.0
    y: float = 0.0  
    z: float = 0.0
    speed: float = 5.0

class Alert(BaseModel):
    drone_id: str
    class_name: str
    confidence: float
    severity: str  # "low", "medium", "high"
    x1: int
    y1: int
    x2: int
    y2: int

detections_store = []
drone_status = {}
alerts_store = []

@router.get("/detections")
def reeive_detection(detection: Detection):
    data = detection.dict()
    data["timestamp"]  = datetime.now().isoformat()
    detections_store.append(data)
    return{"message": "Dtection Received", "total": len(detections_store)}

@router.get("/detections")
def get_detections():
    return {"detections": detections_store}

@router.get("/detections/{drone_id}")
def get_detections_by_drone(drone_id: str):
    filtered = [d for d in detections_store if d["drone_id"] == drone_id]
    return {"drone_id": drone_id, "detections": filtered}

@router.delete("/detections")
def clear_detections():
    detections_store.clear()
    return {"message": "All detections cleared"}

@router.post("/drone/takeoff")
def takeoff(command: DroneCommand):
    result = airsim_takeoff(command.drone_id)
    drone_status[command.drone_id] = "flying"
    return result

@router.post("/drone/land")
def land(command: DroneCommand):
    result = airsim_land(command.drone_id)
    drone_status[command.drone_id] = "landed"
    return result

@router.post("/drone/move")
def move(command: DroneCommand):
    result = airsim_move(
        command.drone_id,
        command.x,
        command.y,
        command.z,
        command.speed
    )
    drone_status[command.drone_id] = "moving"
    return result

@router.post("/drone/return")
def return_to_base(command: DroneCommand):
    result = airsim_return(command.drone_id)
    drone_status[command.drone_id] = "returning"
    return result

@router.post("/alerts")
def create_alert(alert: Alert):
    data = alert.dict()
    data["timestamp"] = datetime.now().isoformat()
    data["resolved"] = False
    data["alert_id"] = len(alerts_store) + 1
    alerts_store.append(data)
    return {"message": "Alert created", "alert_id": data["alert_id"]}

@router.get("/alerts")
def get_alerts():
    return {"alerts": alerts_store}

@router.get("/alerts/active")
def get_active_alerts():
    active = [a for a in alerts_store if not a["resolved"]]
    return {"active_alerts": active, "count": len(active)}

@router.put("/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: int):
    for alert in alerts_store:
        if alert["alert_id"] == alert_id:
            alert["resolved"] = True
            return {"message": f"Alert {alert_id} resolved"}
    return {"message": "Alert not found"}