from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx


app = FastAPI()
ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
SERVICES = {
    "users-app": "http://users-app:8000/api",
    "alarms-app": "http://alarms-app:8000/api",
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
    service_url = SERVICES.get(service)
    if not service_url:
        raise HTTPException(status_code=404, detail="Service not found")

    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
        except:
            JSONResponse({"detail": "Could not parse body JSON"}, status_code=400)

    headers = dict(request.headers)
    response = await forward_request(service_url, request.method, f"/{path}", body, headers)

    try:
        content = response.json()
    except Exception:
        content = {"detail": response.text}

    return JSONResponse(content, response.status_code)
