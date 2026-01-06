// Dashboard JavaScript

let comparisonChart = null;
let distributionChart = null;
let detailsChart = null;

// Color scheme for protocols
const protocolColors = {
    'REST': '#4299e1',
    'gRPC': '#48bb78',
    'Socket.IO': '#f56565',
    'GraphQL': '#ed8936',
    'AVRO': '#9f7aea',
    'CBOR': '#ec4899'
};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadLatest();
    loadRuns();
});

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        document.getElementById('totalRuns').textContent = data.total_runs;
        document.getElementById('totalMetrics').textContent = data.total_metrics.toLocaleString();
        document.getElementById('protocolCount').textContent = Object.keys(data.protocols).length;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load latest results
async function loadLatest() {
    try {
        const response = await fetch('/api/latest');
        const data = await response.json();

        updateComparisonChart(data);
        updateDistributionChart(data);
        showNotification('Latest results loaded');
    } catch (error) {
        console.error('Error loading latest:', error);
        showNotification('Error loading latest results', 'error');
    }
}

// Update comparison chart
function updateComparisonChart(data) {
    const protocols = Object.keys(data);
    const means = protocols.map(p => data[p].stats?.mean || 0);
    const medians = protocols.map(p => data[p].stats?.median || 0);

    const ctx = document.getElementById('comparisonChart');

    if (comparisonChart) {
        comparisonChart.destroy();
    }

    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: protocols,
            datasets: [
                {
                    label: 'Mean Latency (s)',
                    data: means,
                    backgroundColor: protocols.map(p => protocolColors[p] || '#999'),
                    borderColor: protocols.map(p => protocolColors[p] || '#999'),
                    borderWidth: 2
                },
                {
                    label: 'Median Latency (s)',
                    data: medians,
                    backgroundColor: protocols.map(p => protocolColors[p] + '80' || '#99980'),
                    borderColor: protocols.map(p => protocolColors[p] || '#999'),
                    borderWidth: 2,
                    borderDash: [5, 5]
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Latency (seconds)'
                    }
                }
            }
        }
    });
}

// Update distribution chart
function updateDistributionChart(data) {
    const protocols = Object.keys(data);
    const datasets = [];

    for (const protocol of protocols) {
        const stats = data[protocol].stats;
        if (stats) {
            datasets.push({
                label: protocol,
                data: [
                    { x: 'Min', y: stats.min },
                    { x: 'P50', y: stats.p50 || stats.median },
                    { x: 'Mean', y: stats.mean },
                    { x: 'P95', y: stats.p95 },
                    { x: 'P99', y: stats.p99 },
                    { x: 'Max', y: stats.max }
                ],
                borderColor: protocolColors[protocol] || '#999',
                backgroundColor: protocolColors[protocol] + '40' || '#99940',
                tension: 0.4,
                fill: false
            });
        }
    }

    const ctx = document.getElementById('distributionChart');

    if (distributionChart) {
        distributionChart.destroy();
    }

    distributionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Min', 'P50', 'Mean', 'P95', 'P99', 'Max'],
            datasets: datasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Latency (seconds)'
                    }
                }
            }
        }
    });
}

// Load runs table
async function loadRuns(protocol = '') {
    try {
        const url = protocol ? `/api/runs?protocol=${protocol}` : '/api/runs';
        const response = await fetch(url);
        const data = await response.json();

        const tbody = document.getElementById('runsTableBody');
        tbody.innerHTML = '';

        if (data.runs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" class="loading">No runs found</td></tr>';
            return;
        }

        for (const run of data.runs) {
            const row = document.createElement('tr');

            const protocolClass = run.protocol.toLowerCase().replace('.', '');
            const stats = run.stats || {};

            row.innerHTML = `
                <td><span class="protocol-badge badge-${protocolClass}">${run.protocol}</span></td>
                <td>${run.run_id}</td>
                <td>${new Date(run.timestamp).toLocaleString()}</td>
                <td>${stats.mean ? stats.mean.toFixed(6) : 'N/A'}</td>
                <td>${stats.median ? stats.median.toFixed(6) : 'N/A'}</td>
                <td>${stats.p95 ? stats.p95.toFixed(6) : 'N/A'}</td>
                <td>${stats.p99 ? stats.p99.toFixed(6) : 'N/A'}</td>
                <td>${stats.count || 'N/A'}</td>
                <td>
                    <button class="btn btn-info" onclick="viewDetails('${run.run_id}')">View</button>
                    <button class="btn btn-danger" onclick="deleteRun('${run.run_id}')">Delete</button>
                </td>
            `;

            tbody.appendChild(row);
        }
    } catch (error) {
        console.error('Error loading runs:', error);
        showNotification('Error loading runs', 'error');
    }
}

// Filter by protocol
function filterProtocol() {
    const protocol = document.getElementById('protocolFilter').value;
    loadRuns(protocol);
}

// Import legacy results
async function importLegacy() {
    if (!confirm('Import legacy benchmark results from *_out.txt files?')) {
        return;
    }

    try {
        const response = await fetch('/api/import-legacy', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showNotification(data.message);
            loadStats();
            loadLatest();
            loadRuns();
        } else {
            showNotification('Import failed', 'error');
        }
    } catch (error) {
        console.error('Error importing:', error);
        showNotification('Error importing legacy results', 'error');
    }
}

// Delete run
async function deleteRun(runId) {
    if (!confirm(`Delete run ${runId}?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/runs/${runId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showNotification('Run deleted');
            loadStats();
            loadRuns();
        } else {
            showNotification('Delete failed', 'error');
        }
    } catch (error) {
        console.error('Error deleting run:', error);
        showNotification('Error deleting run', 'error');
    }
}

// View run details
async function viewDetails(runId) {
    try {
        const response = await fetch(`/api/runs/${runId}`);
        const data = await response.json();

        document.getElementById('modalTitle').textContent = `${data.protocol} - ${data.run_id}`;

        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <div style="margin-bottom: 20px;">
                <h3>Statistics</h3>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                    <div><strong>Mean:</strong> ${data.stats?.mean.toFixed(6)}s</div>
                    <div><strong>Median:</strong> ${data.stats?.median.toFixed(6)}s</div>
                    <div><strong>Std Dev:</strong> ${data.stats?.std_dev.toFixed(6)}s</div>
                    <div><strong>Min:</strong> ${data.stats?.min.toFixed(6)}s</div>
                    <div><strong>Max:</strong> ${data.stats?.max.toFixed(6)}s</div>
                    <div><strong>Count:</strong> ${data.stats?.count}</div>
                    <div><strong>P95:</strong> ${data.stats?.p95?.toFixed(6)}s</div>
                    <div><strong>P99:</strong> ${data.stats?.p99?.toFixed(6)}s</div>
                </div>
            </div>
        `;

        // Draw detailed chart
        const latencies = data.metrics.map(m => m.latency_seconds);
        const requestIds = data.metrics.map(m => m.request_id);

        const ctx = document.getElementById('detailsChart');

        if (detailsChart) {
            detailsChart.destroy();
        }

        detailsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: requestIds,
                datasets: [{
                    label: 'Latency (s)',
                    data: latencies,
                    borderColor: protocolColors[data.protocol] || '#999',
                    backgroundColor: (protocolColors[data.protocol] || '#999') + '20',
                    borderWidth: 2,
                    pointRadius: 1,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true
                    },
                    title: {
                        display: true,
                        text: 'Latency over Requests'
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Request ID'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Latency (seconds)'
                        }
                    }
                }
            }
        });

        document.getElementById('detailsModal').style.display = 'block';
    } catch (error) {
        console.error('Error loading details:', error);
        showNotification('Error loading run details', 'error');
    }
}

// Close modal
function closeModal() {
    document.getElementById('detailsModal').style.display = 'none';
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('detailsModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}
