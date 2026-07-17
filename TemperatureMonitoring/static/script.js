let tempChart = null;
let refreshInterval = null;

// DOM Elements
const currentTempEl = document.getElementById("currentTemp");
const tempStatusBadge = document.getElementById("tempStatusBadge");
const thermometerBar = document.getElementById("thermometerBar");
const lastUpdatedTimeEl = document.getElementById("lastUpdatedTime");
const tableBodyEl = document.getElementById("tableBody");
const filterStartInp = document.getElementById("filterStart");
const filterEndInp = document.getElementById("filterEnd");
const applyFilterBtn = document.getElementById("applyFilterBtn");
const clearFilterBtn = document.getElementById("clearFilterBtn");
const autoRefreshToggle = document.getElementById("autoRefreshToggle");
const forceReloadBtn = document.getElementById("forceReloadBtn");
const exportCsvBtn = document.getElementById("exportCsvBtn");
const chartStatsText = document.getElementById("chartStatsText");

// Helper to determine status badge class & text
function updateDynamicElements(temp, timestamp) {
    if (!temp) return;

    // Convert to number
    const t = parseFloat(temp);

    // Status text & class
    let statusText = "Normal";
    let statusClass = "badge-normal";
    let tempColor = "var(--temp-normal)";

    if (t < 25.0) {
        statusText = "Cold";
        statusClass = "badge-cold";
        tempColor = "var(--temp-cold)";
    } else if (t >= 25.0 && t < 32.0) {
        statusText = "Normal";
        statusClass = "badge-normal";
        tempColor = "var(--temp-normal)";
    } else if (t >= 32.0 && t < 37.0) {
        statusText = "Warm";
        statusClass = "badge-warm";
        tempColor = "var(--temp-warm)";
    } else {
        statusText = "Hot";
        statusClass = "badge-hot";
        tempColor = "var(--temp-hot)";
    }

    // Set text
    currentTempEl.textContent = t.toFixed(1) + " °C";
    currentTempEl.style.backgroundImage = `linear-gradient(to right, #ffffff, ${tempColor})`;

    // Set badge classes
    tempStatusBadge.textContent = statusText;
    tempStatusBadge.className = "badge " + statusClass;

    // Thermometer percentage: between 20°C (0%) and 40°C (100%)
    let pct = ((t - 20) / 20) * 100;
    pct = Math.max(0, Math.min(100, pct));
    thermometerBar.style.width = pct + "%";
    thermometerBar.style.backgroundColor = tempColor;

    // Last updated time format extracted
    if (timestamp) {
        const parts = timestamp.split(" ");
        lastUpdatedTimeEl.textContent = parts[1] || timestamp;
    }
}

// Fetch and load data
async function loadData() {
    try {
        const startVal = filterStartInp.value;
        const endVal = filterEndInp.value;

        let url = "/temperature";
        const params = [];

        if (startVal) {
            // Format datetimepicker value (YYYY-MM-DDTHH:MM) to matching SQL Time Stamp
            const startFormatted = startVal.replace("T", " ") + ":00";
            params.push(`start=${encodeURIComponent(startFormatted)}`);
        }
        if (endVal) {
            const endFormatted = endVal.replace("T", " ") + ":59";
            params.push(`end=${encodeURIComponent(endFormatted)}`);
        }

        if (params.length > 0) {
            url += "?" + params.join("&");
        }

        const response = await fetch(url);
        if (!response.ok) throw new Error("Server error " + response.status);
        const data = await response.json();

        // Update records length text
        chartStatsText.textContent = `${data.length} logs`;

        // Fill Current Temp card
        if (data.length > 0) {
            updateDynamicElements(data[0].temperature, data[0]["Time Stamp"]);
        } else {
            currentTempEl.textContent = "-- °C";
            tempStatusBadge.textContent = "No data";
            tempStatusBadge.className = "badge text-muted";
            thermometerBar.style.width = "0%";
            lastUpdatedTimeEl.textContent = "--:--:--";
        }

        // Fill Table
        let html = "";
        if (data.length === 0) {
            html = `<tr><td colspan="4" class="text-center text-muted">No records found matching filters.</td></tr>`;
        } else {
            data.forEach(row => {
                html += `
                    <tr>
                        <td>${row.id}</td>
                        <td style="font-weight: 500; font-family: monospace; color: var(--text-primary);">${parseFloat(row.temperature).toFixed(2)} °C</td>
                        <td>${row.date}</td>
                        <td>${row["Time Stamp"]}</td>
                    </tr>
                `;
            });
        }
        tableBodyEl.innerHTML = html;

        // Prepare Chart
        const labels = [];
        const temperatures = [];

        // Ascending order for chart (oldest to newest)
        [...data].reverse().forEach(row => {
            labels.push(row["Time Stamp"]);
            temperatures.push(row.temperature);
        });

        drawChart(labels, temperatures);

    } catch (e) {
        console.error("Error retrieving telemetry data:", e);
    }
}

// Chart.js rendering helper
function drawChart(labels, temperatures) {
    const ctx = document.getElementById("tempChart").getContext("2d");

    if (tempChart !== null) {
        // Update existing chart seamlessly
        tempChart.data.labels = labels;
        tempChart.data.datasets[0].data = temperatures;
        tempChart.update("none");
        return;
    }

    // Create new
    tempChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Temperature (°C)",
                data: temperatures,
                borderColor: "#06b6d4",
                backgroundColor: "rgba(6, 182, 212, 0.08)",
                borderWidth: 3,
                pointBackgroundColor: "#06b6d4",
                pointBorderColor: "#fff",
                pointBorderWidth: 1.5,
                pointRadius: 3,
                pointHoverRadius: 5,
                tension: 0.35,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: "rgba(15, 23, 42, 0.9)",
                    titleFont: { family: "Outfit", size: 12 },
                    bodyFont: { family: "Outfit", size: 13, weight: "bold" },
                    borderColor: "rgba(255,255,255,0.1)",
                    borderWidth: 1,
                    displayColors: false,
                    callbacks: {
                        label: function (context) {
                            return ` ${context.parsed.y.toFixed(2)} °C`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: "rgba(255,255,255,0.03)",
                        borderColor: "rgba(255,255,255,0.05)"
                    },
                    ticks: {
                        color: "#64748b",
                        font: { family: "Outfit", size: 10 },
                        maxRotation: 45,
                        autoSkip: true,
                        maxTicksLimit: 8
                    }
                },
                y: {
                    grid: {
                        color: "rgba(255,255,255,0.03)",
                        borderColor: "rgba(255,255,255,0.05)"
                    },
                    ticks: {
                        color: "#64748b",
                        font: { family: "Outfit", size: 11 }
                    },
                    min: 15,
                    max: 45
                }
            }
        }
    });
}

// Auto-Refresh controller
function toggleAutoRefresh() {
    if (autoRefreshToggle.checked) {
        if (!refreshInterval) {
            refreshInterval = setInterval(loadData, 5000);
        }
    } else {
        if (refreshInterval) {
            clearInterval(refreshInterval);
            refreshInterval = null;
        }
    }
}

// Event Listeners
applyFilterBtn.addEventListener("click", () => {
    loadData();
});

clearFilterBtn.addEventListener("click", () => {
    filterStartInp.value = "";
    filterEndInp.value = "";
    loadData();
});

autoRefreshToggle.addEventListener("change", toggleAutoRefresh);

forceReloadBtn.addEventListener("click", loadData);

exportCsvBtn.addEventListener("click", () => {
    const startVal = filterStartInp.value;
    const endVal = filterEndInp.value;
    let url = "/export-csv";
    const params = [];

    if (startVal) {
        const startFormatted = startVal.replace("T", " ") + ":00";
        params.push(`start=${encodeURIComponent(startFormatted)}`);
    }
    if (endVal) {
        const endFormatted = endVal.replace("T", " ") + ":59";
        params.push(`end=${encodeURIComponent(endFormatted)}`);
    }

    if (params.length > 0) {
        url += "?" + params.join("&");
    }

    window.location.href = url;
});

// Init
loadData();
toggleAutoRefresh();