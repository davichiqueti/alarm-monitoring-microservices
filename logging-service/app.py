from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from pymongo import MongoClient
from datetime import datetime
import os


app = FastAPI()
mongo_client = MongoClient(os.environ["MONGO_CONN_STRING"])
alarm_logs_collection = mongo_client["logs"]["alarms"]


class Log(BaseModel):
    ts: datetime = Field(default_factory=datetime.now)
    alarm: int
    service: str
    detail: dict


@app.api_route("/api/logs/", methods=["POST", "GET"])
async def create_log(request: Request):
    if request.method == "POST":
        log = Log(**await request.json())
        result = alarm_logs_collection.insert_one(log.model_dump())
        return JSONResponse({"inserted_id": str(result.inserted_id)})
    elif request.method == "GET":
        logs = []
        for log in alarm_logs_collection.find():
            log["_id"] = str(log["_id"])
            logs.append(jsonable_encoder(log))
        # Convert ObjectId to string for JSON serialization
        return JSONResponse(logs)
