"""
Baseline values representing normal server behaviour.
"""

# CPU Utilization (%)
CPU_MIN = 5
CPU_MAX = 40

# Memory Utilization (%)
MEMORY_MIN = 20
MEMORY_MAX = 60

# Request Rate (requests/sec)
# Zero is acceptable because the server may simply be idle.
REQUEST_RATE_MIN = 0
REQUEST_RATE_MAX = 15

# Response Time (seconds)
# When there are no requests, response time is naturally 0.0.
RESPONSE_TIME_MIN = 0.00
RESPONSE_TIME_MAX = 0.30


BASELINE = {
    "cpu": {
        "min": CPU_MIN,
        "max": CPU_MAX
    },
    "memory": {
        "min": MEMORY_MIN,
        "max": MEMORY_MAX
    },
    "request_rate": {
        "min": REQUEST_RATE_MIN,
        "max": REQUEST_RATE_MAX
    },
    "response_time": {
        "min": RESPONSE_TIME_MIN,
        "max": RESPONSE_TIME_MAX
    }
}