from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from requests.structures import CaseInsensitiveDict
import os


app = FastAPI()
ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
SERVICES = {
    "users-app": os.environ["USERS_APP_URL"],
    "alarms-app": os.environ["ALARMS_APP_URL"],
    "activation-service": os.environ["ACTIVATION_SERVICE_URL"],
    "trigger-service": os.environ["TRIGGER_SERVICE"],
}


async def forward_request(service_url: str, method: str, path: str, body=None, headers=None, params=None):
    # Avoiding redirect errors on URLs with no "/" on end
    if not path.endswith("/"):
        path += "/"
    url = f"{service_url}{path}"
    if headers:
        headers = CaseInsensitiveDict(headers)
    else:
        headers = {}
    # Setting default headers
    headers["accept"] = "application/json"
    # Letting httpx lib auto set headers that can cause issues
    headers.pop("content-length", None)
    headers.pop("content-type", None)
    headers.pop("host", None)
    # Sending request
    async with httpx.AsyncClient() as client:
        return await client.request(method, url, json=body, headers=headers, params=params)


@app.api_route("/gateway/{service}/{path:path}", methods=ALLOWED_METHODS)
async def gateway(service: str, path: str, request: Request):
    service_url = SERVICES.get(service)
    if not service_url:
        raise HTTPException(status_code=404, detail="Service not found")

    body = None
    if "application/json" in request.headers.get("content-type", ""):
        try:
            body = await request.json()
        except:
            JSONResponse({"detail": "Could not parse body JSON"}, status_code=400)

    response = await forward_request(
        service_url=service_url,
        method=request.method,
        path=f"/{path}",
        body=body,
        headers=request.headers,
        params=dict(request.query_params)
    )

    try:
        content = response.json()
    except Exception:
        content = {"detail": response.text}

    return JSONResponse(content, response.status_code)
