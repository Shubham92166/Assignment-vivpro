import uuid
from fastapi import Request

async def request_id_middleware(request: Request, call_next):
    """Request ID middleware.

    Generates a unique request identifier (UUIDv4) for each incoming HTTP request,
    stores it on `request.state.request_id` for downstream handlers, and attaches
    the same identifier to the outgoing response header `X-Request-ID`.

    Why:
        - Helps correlate logs and traces for a single request across services.
        - Useful for debugging, monitoring, and client visibility.

    Note:
        - The middleware sets `request.state.request_id` (string). Ensure loggers
        or other middlewares read this value before they finish.
    """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
