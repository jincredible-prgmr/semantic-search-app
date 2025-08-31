from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import health, query
from dotenv import load_dotenv
from src.deps import set_chain
from src.retriever import get_rag
from src.core.logging import RequestContextMiddleware, setup_logging
import os



@asynccontextmanager
async def lifespan(app: FastAPI):
    chain = get_rag()
    set_chain(chain)         # stash in a module-level holder for DI
    yield
    # any teardown if needed

def create_app() -> FastAPI:
    app = FastAPI(title="Semantic Search API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("ALLOWED_ORIGINS"),
        allow_methods=["*"], allow_headers=["*"], allow_credentials=True,
    )
    app.include_router(health.router)
    app.include_router(query.router, prefix="/v1")
    return app


load_dotenv()
setup_logging()
app = create_app()
app.add_middleware(RequestContextMiddleware)