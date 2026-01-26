import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status


class RateLimiter:
    def __init__(self, max_requests: int, window_time: int):
        self.max_requests = max_requests
        self.window_time = window_time
        self.requests = defaultdict(deque)

    def is_valid(self, request: Request):
        forwarded_header = request.headers.get("X-Forwarded-For")
        if forwarded_header:
            client_ip = forwarded_header.split(",")[0].strip()
        else:
            client_ip = request.client.host or "unknown"

        now = time.time()
        window_start = now - self.window_time

        # get timestamps of the user associated with the current client ip
        timestamps = self.requests[client_ip]

        # remove timestamps outside the window time (requests older than our window time)
        while timestamps and timestamps[0] < window_start:
            timestamps.popleft()

        # check for max requests a user can make
        if len(timestamps) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later.",
            )

        # place the current request time in timestamps
        timestamps.append(now)
