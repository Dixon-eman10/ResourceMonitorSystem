"""
Detection Rules Module

Defines heuristic rules for detecting
low-rate application-layer DDoS attacks
based on server resource consumption.
"""


def rule_cpu_high_normal_request(analysis):
    """
    Elevated CPU while request rate remains
    relatively low or normal.
    """

    cpu = analysis["cpu"]["value"]
    request_rate = analysis["request_rate"]["value"]

    return (
        cpu >= 25 and
        request_rate <= 20
    )


def rule_slow_http_attack(analysis):
    """
    High response time with relatively
    low or moderate request rate.
    """

    response = analysis["response_time"]["value"]
    request_rate = analysis["request_rate"]["value"]

    return (
        response >= 0.20 and
        request_rate <= 20
    )


def rule_cpu_and_response_high(analysis):
    """
    CPU and response time are both elevated.
    """

    cpu = analysis["cpu"]["value"]
    response = analysis["response_time"]["value"]

    return (
        cpu >= 25 and
        response >= 0.20
    )


def rule_memory_pressure(analysis):
    """
    Elevated memory utilisation.
    """

    memory = analysis["memory"]["value"]

    return memory >= 55


def rule_resource_exhaustion(analysis):
    """
    Resource exhaustion signature.

    Multiple server resources are elevated
    simultaneously.
    """

    cpu = analysis["cpu"]["value"]
    memory = analysis["memory"]["value"]
    response = analysis["response_time"]["value"]

    return (
        cpu >= 25 and
        memory >= 55 and
        response >= 0.20
    )


def rule_high_confidence_attack(analysis):
    """
    High-confidence signature of a
    low-rate application-layer DDoS attack.

    Moderate CPU
    Slow response
    Low/normal request rate
    """

    cpu = analysis["cpu"]["value"]
    response = analysis["response_time"]["value"]
    request_rate = analysis["request_rate"]["value"]

    return (
        cpu >= 20 and
        response >= 0.20 and
        request_rate <= 25
    )