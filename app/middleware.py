import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("manusage")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log incoming request
        logger.info(
            "Incoming request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host,
            }
        )

        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception("Unhandled exception occurred")
            raise e

        # Log outgoing response
        process_time = round((time.time() - start_time) * 1000, 2)
        logger.info(
            "Outgoing response",
            extra={
                "status_code": response.status_code,
                "process_time_ms": process_time,
                "path": request.url.path,
            }
        )

        return response
