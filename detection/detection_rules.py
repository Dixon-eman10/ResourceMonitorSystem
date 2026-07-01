"""
Detection rules for identifying
low-rate application-layer DDoS attacks.
"""


def rule_cpu_high_normal_request(analysis):
    """
    Rule 1:
    CPU High
    Request Rate Normal
    """

    return (
        analysis["cpu"]["status"] == "High"
        and analysis["request_rate"]["status"] == "Normal"
    )


def rule_slow_http_attack(analysis):
    """
    Rule 2:
    High response time
    Low/Normal request rate
    """

    return (
        analysis["response_time"]["status"] == "High"
        and analysis["request_rate"]["status"] in ["Normal", "Idle"]
    )


def rule_resource_exhaustion(analysis):
    """
    Rule 3:
    High CPU and High Memory
    """

    return (
        analysis["cpu"]["status"] == "High"
        and analysis["memory"]["status"] == "High"
    )


def rule_high_confidence_attack(analysis):
    """
    Rule 4:
    CPU, Memory and Response Time are all High
    """

    return (
        analysis["cpu"]["status"] == "High"
        and analysis["memory"]["status"] == "High"
        and analysis["response_time"]["status"] == "High"
    )