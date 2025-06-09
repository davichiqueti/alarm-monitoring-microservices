from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
import httpx
import os


app = FastAPI()


class Trigger(BaseModel):
    ts: datetime = Field(default_factory=datetime.now)
    alarm: int
    spot: str = None


@app.api_route("/api/trigger/", methods=["POST"])
async def trigger_alarm(trigger: Trigger):
    async with httpx.AsyncClient() as client:
        # Checking if alarm exists and is active
        alarm_res = await client.get(f"{os.environ['ALARMS_APP_URL']}/alarms/{trigger.alarm}/")
        if alarm_res.status_code != 200:
            return JSONResponse(
                status_code=alarm_res.status_code,
                content={"detail": f"Error fetching alarm data: {alarm_res.text}"}
            )
        if not alarm_res.json()["active"]:
            return JSONResponse(
                status_code=406,
                content={"detail": "The alarm is not active. So it can't be triggered"}
            )
        # Log Trigger
        trigger_ts = trigger.ts.isoformat()
        log_res = await client.post(
            url=f"{os.environ['LOGGING_SERVICE_URL']}/logs/",
            json={
                "ts": trigger_ts,
                "alarm": trigger.alarm,
                "service": "trigger-service",
                "detail": {
                    "message": f"Alarm triggered. Spot: {trigger.spot}"
                }
            }
        )
        if log_res.status_code != 200:
            return JSONResponse(
                status_code=502,
                content={"detail": f"Logging service error: {log_res.text}"}
            )
        # Calling notification service to notify linked users
        notification_res = await client.post(
            url=f"{os.environ['NOTIFICATION_SERVICE_URL']}/notify/",
            json={
                "ts": trigger_ts,
                "alarm": trigger.alarm,
                "notification_type": "triggered"
            }
        )
        if notification_res.status_code != 200:
            return JSONResponse(
                status_code=502,
                content={"detail": f"Notification service error: {notification_res.text}"}
            )

    return JSONResponse({"detail": "Alarm trigger event logged and Users will be notified"})
