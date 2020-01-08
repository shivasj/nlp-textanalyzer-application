from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from api.routers import articles, artilce_sources, named_entities


prefix = "/api/v1"

# Setup FastAPI app
app = FastAPI(
    title="Text Analyzer Application",
    description="Text Analyzer application",
    version="v1"
)

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception hooks

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": str(exc)
        }
    )

# Application start/stop hooks

@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    pass

# Routes
@app.get(
    "/api",
    summary="Index",
    description="Root api is up!"
)
async def get_index():
    return {
        "message": "Welcome to the Text Analyzer App"
    }

# Additional routers here
app.include_router(articles.router, prefix=prefix)
app.include_router(artilce_sources.router, prefix=prefix)
app.include_router(named_entities.router, prefix=prefix)

app.mount("/", StaticFiles(directory="web", html=True), name="web")
