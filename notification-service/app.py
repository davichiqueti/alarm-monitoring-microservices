from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from core import models, tasks
import os
import httpx


app = FastAPI()


@app.api_route("/api/notify/", methods=["POST"])
async def notify_alarm_event(alarm_notification: models.AlarmNotification):
    alarm_id = alarm_notification.alarm
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{os.environ['alarms-app-url']}/alarms/{alarm_id}/")
        res_json: dict = res.json()
    if res.status_code != 200:
        return JSONResponse(status_code=res.status_code, content=res_json)

    if not res_json["alarm_users"]:
        raise HTTPException(status_code=400, detail=f"None User linked to alarm {alarm_id} to be notified")

    tasks.send_notifications(alarm_data=res_json, notification=alarm_notification)
    return JSONResponse({"detail": "Notifications sended to users linked to the alarm."})
