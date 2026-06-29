import threading
import time
import logging
import psutil

from config.config import MONITORING_INTERVAL
from monitoring import metrics
from database.database import insert_resource_metric


# Configure logging
logging.basicConfig(
    filename="logs/resource_metrics.log",
    level=logging.INFO,
    format="%(asctime)s\nCPU: %(message)s",
)


def collect_metrics():
    """
    Continuously collect server metrics,
    save them to SQLite, and log them.
    """

    while True:

        cpu_usage = psutil.cpu_percent(interval=1)

        memory_usage = psutil.virtual_memory().percent

        request_rate = metrics.request_rate

        response_time = metrics.last_response_time

        # Save to SQLite
        insert_resource_metric(
            cpu=cpu_usage,
            memory=memory_usage,
            request_rate=request_rate,
            response_time=response_time
        )

        # Save to log file
        logging.info(
            f"{cpu_usage:.2f}%\n"
            f"Memory: {memory_usage:.2f}%\n"
            f"Requests/sec: {request_rate}\n"
            f"Response Time: {response_time:.4f} sec\n"
        )

        print("=" * 50)
        print("RESOURCE MONITOR")
        print("=" * 50)
        print(f"CPU Usage       : {cpu_usage:.2f}%")
        print(f"Memory Usage    : {memory_usage:.2f}%")
        print(f"Request Rate    : {request_rate} req/sec")
        print(f"Response Time   : {response_time:.4f} sec")
        print("Status          : Saved to SQLite & Log")
        print()

        time.sleep(MONITORING_INTERVAL)


def start_resource_monitor():
    """
    Starts the monitoring thread.
    """

    monitor_thread = threading.Thread(
        target=collect_metrics,
        daemon=True
    )

    monitor_thread.start()