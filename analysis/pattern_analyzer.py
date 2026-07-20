"""
Pattern Analysis Module

Reads the latest resource metrics and compares them
against the predefined baseline values.
"""

from database.database import fetch_latest_metric
from analysis.baseline import BASELINE


def get_live_metrics():
    """
    Retrieve the latest monitoring metrics.
    """

    metric = fetch_latest_metric()

    if metric is None:
        return None

    return {
        "cpu": metric["cpu"],
        "memory": metric["memory"],
        "request_rate": metric["request_rate"],
        "response_time": metric["response_time"],
        "timestamp": metric["timestamp"]
    }


def get_metric_status(value, minimum, maximum, allow_idle=False):
    """
    Determine the status of a metric.
    """

    if allow_idle and value == 0:
        return "Idle"

    if minimum <= value <= maximum:
        return "Normal"

    if value > maximum:
        return "High"

    return "Low"


def compare_with_baseline(metrics):
    """
    Compare live metrics against baseline values.
    """

    analysis = {
        "cpu": {
            "value": metrics["cpu"],
            "baseline": f'{BASELINE["cpu"]["min"]}-{BASELINE["cpu"]["max"]}%',
            "status": get_metric_status(
                metrics["cpu"],
                BASELINE["cpu"]["min"],
                BASELINE["cpu"]["max"]
            )
        },

        "memory": {
            "value": metrics["memory"],
            "baseline": f'{BASELINE["memory"]["min"]}-{BASELINE["memory"]["max"]}%',
            "status": get_metric_status(
                metrics["memory"],
                BASELINE["memory"]["min"],
                BASELINE["memory"]["max"]
            )
        },

        "request_rate": {
            "value": metrics["request_rate"],
            "baseline": f'{BASELINE["request_rate"]["min"]}-{BASELINE["request_rate"]["max"]} req/sec',
            "status": get_metric_status(
                metrics["request_rate"],
                BASELINE["request_rate"]["min"],
                BASELINE["request_rate"]["max"],
                allow_idle=True
            )
        },

        "response_time": {
            "value": metrics["response_time"],
            "baseline": f'{BASELINE["response_time"]["min"]:.2f}-{BASELINE["response_time"]["max"]:.2f} sec',
            "status": get_metric_status(
                metrics["response_time"],
                BASELINE["response_time"]["min"],
                BASELINE["response_time"]["max"],
                allow_idle=True
            )
        }
    }

    return analysis


def classify_pattern(analysis):
    """
    Determine the overall resource consumption pattern.
    """

    abnormal_metrics = []

    for metric, result in analysis.items():
        if result["status"] == "High":
            abnormal_metrics.append(metric)

    if len(abnormal_metrics) >= 2:
        overall_status = "Suspicious"
    else:
        overall_status = "Normal"

    return {
        "overall_status": overall_status,
        "abnormal_metrics": abnormal_metrics
    }


def analyze_pattern():
    """
    Perform a complete pattern analysis and return the result.
    This function will be called by the Detection Engine.
    """

    metrics = get_live_metrics()

    if metrics is None:
        return None

    analysis = compare_with_baseline(metrics)
    pattern = classify_pattern(analysis)

    return {
        "timestamp": metrics["timestamp"],
        "metrics": metrics,
        "analysis": analysis,
        "pattern": pattern
    }


if __name__ == "__main__":

    result = analyze_pattern()

    if result is None:
        print("No monitoring data found.")
        exit()

    print("\n========== LIVE METRICS ==========")
    print(result["metrics"])

    print("\n====== PATTERN ANALYSIS ======")

    for metric, details in result["analysis"].items():
        print(
            f"{metric.upper():15}"
            f" Value: {details['value']}"
            f" | Baseline: {details['baseline']}"
            f" | Status: {details['status']}"
        )

    print("\n====== OVERALL RESULT ======")
    print(f"Pattern Status   : {result['pattern']['overall_status']}")
    print(f"Abnormal Metrics : {result['pattern']['abnormal_metrics']}")