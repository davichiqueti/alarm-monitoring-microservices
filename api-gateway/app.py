from fastapi import FastAPI, APIRouter, Request, Response
import httpx


app = FastAPI()
users_router = APIRouter(prefix="/api/users-app", tags=["users"])

@users_router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_users(request: Request, path: str):
    url = f"http://users-app:8000/{path}"
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            content=await request.body(),
            params=dict(request.query_params)
        )
    return Response(content=resp.content, status_code=resp.status_code, headers=dict(resp.headers))

app.include_router(users_router)
