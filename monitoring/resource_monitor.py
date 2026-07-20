"""
Resource Monitoring Module

Continuously collects system resource metrics,
stores them in the SQLite database,
writes them to a log file,
and periodically removes old monitoring records.
"""

import threading
import time
import logging

import psutil

from config.config import MONITORING_INTERVAL
from monitoring import metrics
from database.database import (
    insert_resource_metric,
    cleanup_old_metrics
)


# ==========================================================
# Logging Configuration
# ==========================================================

logging.basicConfig(
    filename="logs/resource_metrics.log",
    level=logging.INFO,
    format="%(asctime)s\nCPU: %(message)s",
    force=True
)


# ==========================================================
# Resource Monitoring
# ==========================================================

def collect_metrics():
    """
    Continuously collect server metrics,
    save them to SQLite,
    write them to the log file,
    and periodically clean old monitoring records.
    """

    # Prime CPU measurement
    psutil.cpu_percent(interval=None)

    last_cleanup = time.time()

    while True:

        # Sample CPU over the monitoring interval
        cpu_usage = psutil.cpu_percent(interval=MONITORING_INTERVAL)

        memory_usage = psutil.virtual_memory().percent

        request_rate = metrics.request_rate

        # Use the highest response time observed
        response_time = metrics.max_response_time

        # Prepare for next monitoring interval
        metrics.max_response_time = 0.0

        # Save metrics
        insert_resource_metric(
            cpu=cpu_usage,
            memory=memory_usage,
            request_rate=request_rate,
            response_time=response_time
        )

        # Log metrics
        logging.info(
            f"{cpu_usage:.2f}%\n"
            f"Memory: {memory_usage:.2f}%\n"
            f"Requests/sec: {request_rate}\n"
            f"Response Time: {response_time:.3f} sec\n"
        )

        # Remove old records every 30 minutes
        if time.time() - last_cleanup >= 1800:

            cleanup_old_metrics(minutes=30)

            print("Old monitoring records removed.")

            last_cleanup = time.time()

        # Console output
        print("=" * 50)
        print("RESOURCE MONITOR")
        print("=" * 50)
        print(f"CPU Usage       : {cpu_usage:.2f}%")
        print(f"Memory Usage    : {memory_usage:.2f}%")
        print(f"Request Rate    : {request_rate} req/sec")
        print(f"Response Time   : {response_time:.3f} sec")
        print("Status          : Saved to SQLite & Log")
        print()


# ==========================================================
# Start Monitoring Thread
# ==========================================================

def start_resource_monitor():
    """
    Start the resource monitoring daemon thread.
    """

    monitor_thread = threading.Thread(
        target=collect_metrics,
        daemon=True,
        name="ResourceMonitor"
    )

    monitor_thread.start()