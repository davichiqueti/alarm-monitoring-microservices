from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx


app = FastAPI()
ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
SERVICES = {
    "users-app": "http://users-app:8000",
}


async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    # Avoiding redirect errors on URLs with no "/" on end
    if not path.endswith("/"):
        path += "/"
    url = f"{service_url}{path}?format=json"
    if headers:
        # Letting content metadata definition be auto set to avoid errors
        headers.pop("content-length", None)
        headers.pop("content-type", None)
    # Sending request
    async with httpx.AsyncClient() as client:
        return await client.request(method, url, json=body, headers=headers)


@app.api_route("/{service}/{path:path}", methods=ALLOWED_METHODS)
async def gateway(service: str, path: str, request: Request):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    service_url = SERVICES[service]
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.json()
    headers = dict(request.headers)
    response = await forward_request(service_url, request.method, f"/{path}", body, headers)

    try:
        content = response.json()
    except Exception:
        content = {"detail": response.text}

    return JSONResponse(content, response.status_code)
