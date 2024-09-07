from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

origins = ["http://localhost:11434"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class RateLimiter:
    def __init__(self):
        self.requests = 0

    async def __call__(self, request: Request):
        if request.method == "POST":
            if self.requests < 10:
                self.requests += 1
                return await next(self)
            else:
                return JSONResponse({"error": "Rate limit exceeded"}, status_code=429)

app.middleware("http", RateLimiter())


# Sample route
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}


class DemoPostData(BaseModel):
    data: str


@app.post("/demo_post")
async def demo_post(post_data: DemoPostData):
    return {"message": f"Received data: {post_data.data}"}
