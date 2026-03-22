AIRSIM_ENABLED = False  # Change karna h true when real airsim ho

#real vale functions for airsim
def get_client(drone_id: str):
    """Connect to AirSim and return client."""
    import airsim
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True, drone_id)
    client.armDisarm(True, drone_id)
    return client


def airsim_takeoff(drone_id: str):
    if not AIRSIM_ENABLED:
        return simulate_response(drone_id, "takeoff")
    try:
        client = get_client(drone_id)
        client.takeoffAsync(vehicle_name=drone_id).join()
        return {"success": True, "drone_id": drone_id, "action": "takeoff"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def airsim_land(drone_id: str):
    if not AIRSIM_ENABLED:
        return simulate_response(drone_id, "land")
    try:
        client = get_client(drone_id)
        client.landAsync(vehicle_name=drone_id).join()
        return {"success": True, "drone_id": drone_id, "action": "land"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def airsim_move(drone_id: str, x: float, y: float, z: float, speed: float):
    if not AIRSIM_ENABLED:
        return simulate_response(drone_id, "move", x=x, y=y, z=z)
    try:
        client = get_client(drone_id)
        client.moveToPositionAsync(
            x, y, z, speed, vehicle_name=drone_id
        ).join()
        return {"success": True, "drone_id": drone_id, "action": "move",
                "target": {"x": x, "y": y, "z": z}}
    except Exception as e:
        return {"success": False, "error": str(e)}


def airsim_return(drone_id: str):
    if not AIRSIM_ENABLED:
        return simulate_response(drone_id, "return")
    try:
        client = get_client(drone_id)
        client.moveToPositionAsync(
            0, 0, -10, 5, vehicle_name=drone_id
        ).join()
        return {"success": True, "drone_id": drone_id, "action": "return"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# fake response
def simulate_response(drone_id: str, action: str, **kwargs):
    response = {
        "success": True,
        "drone_id": drone_id,
        "action": action,
        "mode": "simulation"
    }
    if kwargs:
        response["target"] = kwargs
    return response