import uuid, time, logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = str(uuid.uuid4())
        start = time.perf_counter()
        # make ID available to handlers & return it to client
        request.state.request_id = rid
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        # fallback latency logging for non-/v1/query routes
        dur_ms = int((time.perf_counter() - start) * 1000)
        logging.info(f"rid={rid} method={request.method} path={request.url.path} status={response.status_code} ms={dur_ms}")
        return response
    
def setup_logging():
    """Configure global logging for the app."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    # Optional: quiet noisy loggers like httpx/uvicorn.access
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.info("Logging initialized")