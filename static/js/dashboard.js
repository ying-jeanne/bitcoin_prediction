let priceChart;

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    setInterval(updateDashboard, 30000); // Update every 30 seconds
});

async function initializeDashboard() {
    await updatePrice();
    await updatePrediction();
    await initializeChart();
}

async function updatePrice() {
    try {
        const response = await fetch('/api/price');
        const data = await response.json();
        
        document.getElementById('currentPrice').textContent = `$${data.price.toLocaleString()}`;
        
        const changeElement = document.getElementById('priceChange');
        const changeText = `${data.change_24h >= 0 ? '↗' : '↘'} ${data.change_24h.toFixed(2)}%`;
        const changeAmount = `($${Math.abs(data.change_24h_amount).toLocaleString()})`;
        
        changeElement.innerHTML = `
            <span class="${data.change_24h >= 0 ? 'positive' : 'negative'}">${changeText}</span>
            <span>${changeAmount}</span>
        `;
    } catch (error) {
        console.error('Error updating price:', error);
    }
}

async function updatePrediction() {
    try {
        const response = await fetch('/api/prediction');
        const data = await response.json();

        // Update prediction badge and scores
        const badge = document.getElementById('predictionBadge');
        badge.textContent = data.prediction.replace('_', ' ');
        badge.className = `prediction-badge ${data.prediction.replace('_', '-')}`;

        document.getElementById('confidenceScore').textContent = `Confidence: ${data.confidence}%`;
        document.getElementById('technicalScore').textContent = `${Math.round(data.technical_score)}/100`;
        document.getElementById('sentimentScore').textContent = `${Math.round(data.sentiment_score)}/100`;

        // Update indicators
        updateIndicators(data.indicators);

        // Update news sentiment
        updateNewsSentiment(data.news_sentiment);

    } catch (error) {
        console.error('Error updating prediction:', error);
    }
}

function updateIndicators(indicators) {
    const indicatorsGrid = document.getElementById('indicatorsGrid');
    indicatorsGrid.innerHTML = '';
    
    const indicatorsList = [
        { key: 'rsi', title: 'RSI (14)' },
        { key: 'macd', title: 'MACD' },
        { key: 'bollinger_bands', title: 'Bollinger Bands' },
        { key: 'volume', title: 'Volume' }
    ];
    
    indicatorsList.forEach(indicator => {
        const data = indicators[indicator.key];
        const card = document.createElement('div');
        card.className = 'indicator-card';
        card.innerHTML = `
            <div class="indicator-header">
                <div class="indicator-title">${indicator.title}</div>
            </div>
            <div class="indicator-value">${data.value}</div>
            <div class="indicator-signal ${data.signal_class}">${data.signal}</div>
        `;
        indicatorsGrid.appendChild(card);
    });
}

function updateNewsSentiment(newsItems) {
    const newsList = document.getElementById('newsList');
    const sentimentScore = document.getElementById('overallSentiment');
    
    // Calculate average sentiment
    let totalSentiment = 0;
    newsItems.forEach(item => {
        totalSentiment += item.sentiment === 'Positive' ? 1 : (item.sentiment === 'Negative' ? -1 : 0);
    });
    const avgSentiment = totalSentiment / newsItems.length;
    
    sentimentScore.textContent = avgSentiment >= 0 ? `+${avgSentiment.toFixed(2)}` : avgSentiment.toFixed(2);
    sentimentScore.className = `sentiment-score ${avgSentiment >= 0 ? 'bullish' : 'bearish'}`;
    
    // Update news items
    newsList.innerHTML = '';
    newsItems.forEach(item => {
        const newsItem = document.createElement('div');
        newsItem.className = 'news-item';
        newsItem.innerHTML = `
            <div class="news-title">${item.title}</div>
            <div class="news-meta">
                <span>${item.time_ago}</span>
                <span class="${item.sentiment_class}">${item.sentiment}</span>
            </div>
        `;
        newsList.appendChild(newsItem);
    });
}

async function initializeChart() {
    try {
        const response = await fetch('/api/chart-data');
        const data = await response.json();
        
        const ctx = document.getElementById('priceChart').getContext('2d');
        priceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Bitcoin Price',
                    data: data.prices,
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error initializing chart:', error);
    }
}

async function updateDashboard() {
    await updatePrice();
    await updatePrediction();
    
    // Update chart data
    if (priceChart) {
        try {
            const response = await fetch('/api/chart-data');
            const data = await response.json();
            
            priceChart.data.labels = data.labels;
            priceChart.data.datasets[0].data = data.prices;
            priceChart.update();
        } catch (error) {
            console.error('Error updating chart:', error);
        }
    }
}

async function refreshAnalysis() {
    const btn = document.querySelector('.refresh-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '⏳ Analyzing...';
    btn.disabled = true;
    
    try {
        await updatePrediction();
        
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }, 2000);
    } catch (error) {
        console.error('Error refreshing analysis:', error);
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}
