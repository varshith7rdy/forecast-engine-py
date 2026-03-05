let chartInstance = null;

function toggleDarkMode() {
    document.body.classList.toggle('dark');
}

function sendPrediction() {
    const query = document.getElementById('query').value.trim();
    const resultsDiv = document.getElementById('results');

    if (!query) {
        resultsDiv.innerHTML = '<div class="error">Please enter a query</div>';
        return;
    }

    resultsDiv.innerHTML = '<p>Loading...</p>';

    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            query: query
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultsDiv.innerHTML = `<div class="error"><strong>Error:</strong> ${data.error}</div>`;
        } else {
            displayResults(data);
        }
    })
    .catch(error => {
        resultsDiv.innerHTML = `<div class="error"><strong>Error:</strong> ${error.message}</div>`;
        console.error('Error:', error);
    });
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    let resultsHTML = '';

    if (data.predicted_orders !== undefined) {
        
        const prediction = Math.round(data.predicted_orders);
        resultsHTML = `
            <div class="prediction-result">
                <h3>Prediction Results</h3>
                <p><strong>Restaurant ID:</strong> ${data.restaurant_id}</p>
                <p><strong>Target Date:</strong> ${data.target_date}</p>
                <p style="font-size: 24px; color: #2e7d32;"><strong>Predicted Orders: ${prediction}</strong></p>
            </div>
        `;
    } else if (data.chartdata && Object.keys(data.chartdata).length > 0) {
        
        resultsHTML = `
            <div class="prediction-result">
                <h3>Historical Data Results</h3>
                <p><strong>Total Records:</strong> ${data.total_records || Object.keys(data.chartdata).length}</p>
                <p style="font-size: 18px; color: #2e7d32;"><strong>Date Range Available</strong></p>
            </div>
        `;
    }

    if (data.chartdata && Object.keys(data.chartdata).length > 0) {
        resultsHTML += '<div class="chart-container"><canvas id="orderChart"></canvas></div>';
    }

    resultsDiv.innerHTML = resultsHTML;

    if (data.chartdata && Object.keys(data.chartdata).length > 0) {
        setTimeout(() => {
            displayChart(data.chartdata);
        }, 100);
    }
}

function displayChart(chartdata) {
    const ctx = document.getElementById('orderChart');
    if (!ctx) return;

    const dates = Object.keys(chartdata).sort();
    const orders = dates.map(date => chartdata[date]);

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Historical Orders',
                data: orders,
                borderColor: '#2196F3',
                backgroundColor: 'rgba(33, 150, 243, 0.1)',
                tension: 0.3,
                fill: true,
                pointRadius: 3,
                pointBackgroundColor: '#2196F3',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Order History',
                    font: { size: 16 }
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Orders' }
                },
                x: {
                    title: { display: true, text: 'Date' },
                    ticks: {
                        maxTicksLimit: 10
                    }
                }
            }
        }
    });
}
