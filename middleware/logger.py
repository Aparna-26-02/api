import time
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def log_time(request, call_next):
    start = time.time()
    logging.info(f"Request Started: {request.method} {request.url}")

    response = await call_next(request)

    process_time = time.time() - start
    logging.info(f"Request Time: {process_time:.4f} sec")

    return response