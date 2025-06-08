from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel


app = FastAPI()

class ActivationStatus(BaseModel):
    active: bool


@app.api_route("/api/", methods=["GET"])
async def get_alarms_activation_status():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"http://alarms-app:8000/api/alarms/")
    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.text)

    alarms_data = res.json()
    alarms_status = {alarm["id"]: alarm["active"] for alarm in alarms_data}
    return JSONResponse({"alarms-status": alarms_status})


@app.api_route("/api/{alarm_id}/", methods=["POST"])
async def update_alarm_activation_status(alarm_id: int, status: ActivationStatus):
    async with httpx.AsyncClient() as client:
        res = await client.patch(
            url=f"http://alarms-app:8000/api/alarms/{alarm_id}/",
            json={"active": status.active}
        )
    if res.status_code != 200:
        return JSONResponse(status_code=res.status_code, content=res.json())

    return JSONResponse({"detail": {"message": "Alarm activation status updated successfully"}})
