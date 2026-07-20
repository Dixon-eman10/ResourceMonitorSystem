"""
Shared monitoring metrics.

These values are updated by the Request Tracker
and read by the Resource Monitoring Module.
"""

# --------------------------------------------------
# Request statistics
# --------------------------------------------------

request_count = 0
request_rate = 0

# --------------------------------------------------
# Response time statistics
# --------------------------------------------------

# Last completed request
last_response_time = 0.0

# Highest response time observed
# during the current one-second window.
max_response_time = 0.0

# Average response time
response_total = 0.0
response_samples = 0
average_response_time = 0.0