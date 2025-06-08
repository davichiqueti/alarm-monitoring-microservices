from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel
import os

app = FastAPI()
ALARMS_APP_URL = os.environ["ALARMS_APP_URL"]


class AlarmActivationStatus(BaseModel):
    alarm: int
    status: bool


@app.api_route("/api/", methods=["GET"])
async def get_alarms_activation_status():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{ALARMS_APP_URL}/alarms/")
    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.text)

    alarms_data = res.json()
    alarms_status = {alarm["id"]: alarm["active"] for alarm in alarms_data}
    return JSONResponse({"alarms-status": alarms_status})


@app.api_route("/api/status/", methods=["POST"])
async def set_activation_status(activation_status: AlarmActivationStatus):
    async with httpx.AsyncClient() as client:
        res = await client.patch(
            url=f"{ALARMS_APP_URL}/alarms/{activation_status.alarm}/",
            json={"active": activation_status.status}
        )
    if res.status_code != 200:
        return JSONResponse(status_code=res.status_code, content=res.json())

    return JSONResponse({"detail": "Alarm activation status updated successfully"})
