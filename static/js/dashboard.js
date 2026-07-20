// ======================================================
// Administrator Dashboard
// Live Update Controller
// ======================================================

// ------------------------------------------------------
// Chart Variables
// ------------------------------------------------------

let cpuChart;
let memoryChart;
let requestChart;
let responseChart;

let labels = [];

let cpuData = [];
let memoryData = [];
let requestData = [];
let responseData = [];


// ------------------------------------------------------
// Create Chart
// ------------------------------------------------------

function createChart(canvasId, label, dataArray) {

    return new Chart(
        document.getElementById(canvasId),
        {
            type: "line",

            data: {

                labels: labels,

                datasets: [

                    {

                        label: label,

                        data: dataArray,

                        fill: false,

                        tension: 0.3

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: false,

                plugins: {

                    legend: {

                        display: true

                    }

                }

            }

        }
    );

}


// ------------------------------------------------------
// Initialize Dashboard
// ------------------------------------------------------

window.onload = function () {

    cpuChart = createChart(
        "cpuChart",
        "CPU Usage (%)",
        cpuData
    );

    memoryChart = createChart(
        "memoryChart",
        "Memory Usage (%)",
        memoryData
    );

    requestChart = createChart(
        "requestChart",
        "Requests / Second",
        requestData
    );

    responseChart = createChart(
        "responseChart",
        "Response Time (sec)",
        responseData
    );

    refreshDashboard();

    setInterval(
        refreshDashboard,
        3000
    );

};


// ------------------------------------------------------
// Retrieve Latest Dashboard Data
// ------------------------------------------------------

function refreshDashboard() {

    fetch("/api/dashboard-data")

        .then(response => response.json())

        .then(data => {

            updateCards(data.latest_metric);

            updateStatus(data);

            updateCharts(data.recent_metrics);

            updateAlerts(data.alerts);

            updateIncidentLogs(data.incident_logs);

        })

        .catch(error => {

            console.error("Dashboard refresh failed:", error);

        });

}


// ------------------------------------------------------
// Summary Cards
// ------------------------------------------------------

function updateCards(metric) {

    if (!metric)
        return;

    document.getElementById("cpu-value").textContent =
        `${metric.cpu.toFixed(1)}%`;

    document.getElementById("memory-value").textContent =
        `${metric.memory.toFixed(1)}%`;

    document.getElementById("request-value").textContent =
        metric.request_rate;

    document.getElementById("response-value").textContent =
        `${metric.response_time.toFixed(3)} sec`;

}


// ------------------------------------------------------
// Detection Status
// ------------------------------------------------------

function updateStatus(data) {

    const status =
        document.getElementById("system-status");

    status.innerHTML = `
        <strong>${data.system_status}</strong><br>
        Decision: ${data.decision}<br>
        Severity: ${data.severity}
    `;

    if (data.decision === "Attack Detected") {

        status.style.background = "#c62828";

    }

    else {

        status.style.background = "#16a34a";

    }

}


// ------------------------------------------------------
// Charts
// ------------------------------------------------------

function updateCharts(metrics) {

    if (!metrics || metrics.length === 0)
        return;

    labels.length = 0;

    cpuData.length = 0;

    memoryData.length = 0;

    requestData.length = 0;

    responseData.length = 0;

    metrics.forEach(metric => {

        labels.push(metric.timestamp.split(" ")[1]);

        cpuData.push(metric.cpu);

        memoryData.push(metric.memory);

        requestData.push(metric.request_rate);

        responseData.push(metric.response_time);

    });

    cpuChart.update();

    memoryChart.update();

    requestChart.update();

    responseChart.update();

}


// ------------------------------------------------------
// Active Alerts
// ------------------------------------------------------

function updateAlerts(alerts) {

    const body =
        document.getElementById("alerts-body");

    body.innerHTML = "";

    if (alerts.length === 0) {

        body.innerHTML = `

            <tr>

                <td colspan="3">

                    No Active Alerts

                </td>

            </tr>

        `;

        return;

    }

    alerts.forEach(alert => {

        body.innerHTML += `

            <tr>

                <td>${alert[4]}</td>

                <td>${alert[2]}</td>

                <td>${alert[3]}</td>

            </tr>

        `;

    });

}


// ------------------------------------------------------
// Incident Logs
// ------------------------------------------------------

function updateIncidentLogs(logs) {

    const body =
        document.getElementById("incident-body");

    body.innerHTML = "";

    if (logs.length === 0) {

        body.innerHTML = `

            <tr>

                <td colspan="3">

                    No Incident Logs

                </td>

            </tr>

        `;

        return;

    }

    logs.forEach(log => {

        body.innerHTML += `

            <tr>

                <td>${log[3]}</td>

                <td>${log[2]}</td>

                <td>${log[1]}</td>

            </tr>

        `;

    });

}