from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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


@app.api_route("/api/logs/", methods=["POST"])
async def create_log(log: Log):
    result = alarm_logs_collection.insert_one(log.model_dump())
    return JSONResponse({"inserted_id": str(result.inserted_id)})
