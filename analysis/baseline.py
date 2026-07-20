"""
Baseline values representing normal server behaviour.

These values were established experimentally by observing
the system under normal (non-attack) conditions.
"""

# ==========================================================
# CPU Utilization (%)
# ==========================================================

# Normal CPU fluctuated between about 5% and 35%.
# Values above this indicate abnormal processing.

CPU_MIN = 0
CPU_MAX = 35


# ==========================================================
# Memory Utilization (%)
# ==========================================================

# Memory remained relatively stable.

MEMORY_MIN = 20
MEMORY_MAX = 60


# ==========================================================
# Request Rate (requests/sec)
# ==========================================================

# Low-rate attacks intentionally generate only a few requests.

REQUEST_RATE_MIN = 0
REQUEST_RATE_MAX = 10


# ==========================================================
# Response Time (seconds)
# ==========================================================

# Normal responses are almost instantaneous.
# Values above 0.5 seconds indicate abnormal processing.

RESPONSE_TIME_MIN = 0.00
RESPONSE_TIME_MAX = 0.50


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