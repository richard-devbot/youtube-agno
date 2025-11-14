"""
Rate limiting middleware with exponential backoff for research workflow.
"""

import time
from collections import defaultdict, deque
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class AdaptiveRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, 
        app,
        requests_per_minute: int = 60,
        max_backoff_time: int = 30,
        min_backoff_time: int = 2
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.max_backoff_time = max_backoff_time
        self.min_backoff_time = min_backoff_time
        self.request_history = defaultdict(lambda: deque())
        self.error_counts = defaultdict(int)
        self.backoff_until = defaultdict(float)

    def calculate_backoff(self, error_count: int) -> float:
        """Calculate exponential backoff time based on error count."""
        backoff_time = min(
            self.max_backoff_time,
            self.min_backoff_time * (2 ** error_count)
        )
        return time.time() + backoff_time

    def is_rate_limited(self, client_ip: str) -> bool:
        """Check if the client is currently rate limited."""
        current_time = time.time()
        
        # Check if in backoff period
        if current_time < self.backoff_until[client_ip]:
            wait_time = self.backoff_until[client_ip] - current_time
            logger.warning(f"Client {client_ip} in backoff period. Wait {wait_time:.1f}s")
            return True

        # Clean old requests
        history = self.request_history[client_ip]
        while history and current_time - history[0] > 60:
            history.popleft()

        # Check rate limit
        return len(history) >= self.requests_per_minute

    def handle_429(self, client_ip: str):
        """Handle a 429 response by increasing backoff."""
        self.error_counts[client_ip] += 1
        self.backoff_until[client_ip] = self.calculate_backoff(
            self.error_counts[client_ip]
        )
        logger.warning(
            f"Rate limit hit for {client_ip}. "
            f"Error count: {self.error_counts[client_ip]}, "
            f"Backoff until: {self.backoff_until[client_ip]}"
        )

    def handle_success(self, client_ip: str):
        """Handle a successful request by reducing error count."""
        if self.error_counts[client_ip] > 0:
            self.error_counts[client_ip] = max(0, self.error_counts[client_ip] - 1)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Check rate limiting
        if self.is_rate_limited(client_ip):
            backoff_time = max(0, self.backoff_until[client_ip] - current_time)
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "retry_after": backoff_time,
                    "type": "rate_limit"
                }
            )

        # Track request
        self.request_history[client_ip].append(current_time)

        # Process request
        try:
            response = await call_next(request)
            
            # Handle response status
            if response.status_code == 429:
                self.handle_429(client_ip)
            elif response.status_code < 400:
                self.handle_success(client_ip)
                
            return response
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error", "type": "internal_error"}
            )