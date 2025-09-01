from flask import Flask, render_template, jsonify
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random
from models.technical_analysis import TechnicalAnalysis
from models.sentiment_analysis import SentimentAnalysis
from models.prediction_model import PredictionModel

app = Flask(__name__)

# Initialize analysis models
technical_analyzer = TechnicalAnalysis()
sentiment_analyzer = SentimentAnalysis()
prediction_model = PredictionModel()

@app.route('/')
def dashboard():
    """Render the main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/prediction')
def get_prediction():
    """Get combined prediction from technical and sentiment analysis"""
    # --- MOCK DATA FOR FRONTEND ---
    # try:
    #     # Get current Bitcoin price data
    #     price_data = get_bitcoin_price_history()
    #     # Perform technical analysis
    #     technical_score = technical_analyzer.analyze(price_data)
    #     # Perform sentiment analysis
    #     sentiment_score = sentiment_analyzer.analyze()
    #     # Generate prediction
    #     prediction = prediction_model.predict(technical_score, sentiment_score)
    #     return jsonify({
    #         'prediction': prediction['signal'],
    #         'confidence': prediction['confidence'],
    #         'technical_score': technical_score['overall_score'],
    #         'sentiment_score': sentiment_score['score'],
    #         'indicators': technical_score['indicators'],
    #         'news_sentiment': sentiment_score['news_items'],
    #         'timestamp': datetime.now().isoformat()
    #     })
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
    return jsonify({
        'prediction': 'buy',
        'confidence': 87,
        'technical_score': 75,
        'sentiment_score': 65,
        'indicators': {
            'rsi': {'value': 55, 'signal': 'Neutral', 'signal_class': 'neutral'},
            'macd': {'value': 1.2, 'signal': 'Bullish', 'signal_class': 'bullish'},
            'bollinger_bands': {'value': 'Wide', 'signal': 'Volatile', 'signal_class': 'volatile'},
            'volume': {'value': '1.2B', 'signal': 'High', 'signal_class': 'bullish'}
        },
        'news_sentiment': [
            {
                'title': 'Bitcoin surges as market rallies',
                'sentiment': 'Positive',
                'sentiment_class': 'bullish',
                'time_ago': '2h ago'
            },
            {
                'title': 'Analysts predict bullish trend',
                'sentiment': 'Positive',
                'sentiment_class': 'bullish',
                'time_ago': '1h ago'
            },
            {
                'title': 'Regulatory uncertainty remains',
                'sentiment': 'Neutral',
                'sentiment_class': 'neutral',
                'time_ago': '30m ago'
            }
        ],
        'timestamp': datetime.now().isoformat(),
        # Additional fields for frontend
        'predictionBadge': 'Buy',
        'confidenceScore': 'Confidence: 87%',
        'technicalScore': '75/100',
        'sentimentScore': '65/100',
        'volumeAnalysis': 'High',
        'marketMomentum': 'Bullish'
    })

@app.route('/api/price')
def get_current_price():
    """Get current Bitcoin price"""
    # --- MOCK DATA FOR FRONTEND ---
    # try:
    #     response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true')
    #     data = response.json()
    #     btc_data = data['bitcoin']
    #     price = btc_data['usd']
    #     change_24h = btc_data['usd_24h_change']
    #     return jsonify({
    #         'price': price,
    #         'change_24h': change_24h,
    #         'change_24h_amount': price * change_24h / 100,
    #         'timestamp': datetime.now().isoformat()
    #     })
    # except Exception as e:
    #     # Fallback to demo data if API fails
    #     return jsonify({
    #         'price': 67234.50,
    #         'change_24h': 2.34,
    #         'change_24h_amount': 1567.89,
    #         'timestamp': datetime.now().isoformat()
    #     })
    return jsonify({
        'price': 67234.50,
        'change_24h': 2.34,
        'change_24h_amount': 1567.89,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/chart-data')
def get_chart_data():
    """Get price chart data"""
    # --- MOCK DATA FOR FRONTEND ---
    # try:
    #     # Get 24 hours of price data
    #     price_history = get_bitcoin_price_history(days=1)
    #     return jsonify(price_history)
    # except Exception as e:
    #     # Fallback demo data
    #     hours = [(datetime.now() - timedelta(hours=i)).strftime('%H:%M') for i in range(24, 0, -1)]
    #     prices = [65200 + random.randint(-2000, 2000) for _ in range(24)]
    #     return jsonify({
    #         'labels': hours,
    #         'prices': prices
    #     })
    hours = [(datetime.now() - timedelta(hours=i)).strftime('%H:%M') for i in range(24, 0, -1)]
    prices = [65200 + random.randint(-2000, 2000) for _ in range(24)]
    return jsonify({
        'labels': hours,
        'prices': prices
    })

def get_bitcoin_price_history(days=30):
    # """Fetch Bitcoin price history"""
    # try:
    #     url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={days}'
    #     response = requests.get(url)
    #     data = response.json()
        
    #     # Extract prices and timestamps
    #     prices = [item[1] for item in data['prices']]
    #     timestamps = [datetime.fromtimestamp(item[0]/1000) for item in data['prices']]
        
    #     return {
    #         'prices': prices,
    #         'timestamps': timestamps,
    #         'volumes': [item[1] for item in data['total_volumes']]
    #     }
    # except Exception as e:
    #     print(f"Error fetching price history: {e}")
    #     # Return demo data
    return generate_demo_price_data(days)

def generate_demo_price_data(days=30):
    """Generate demo price data for testing"""
    base_price = 67000
    prices = []
    timestamps = []
    volumes = []
    
    for i in range(days * 24):  # Hourly data
        timestamp = datetime.now() - timedelta(hours=i)
        price = base_price + random.randint(-5000, 5000) + np.sin(i/12) * 1000
        volume = random.randint(100000000, 2000000000)
        
        prices.append(price)
        timestamps.append(timestamp)
        volumes.append(volume)
    
    return {
        'prices': list(reversed(prices)),
        'timestamps': list(reversed(timestamps)),
        'volumes': list(reversed(volumes))
    }

if __name__ == '__main__':
    app.run(debug=True)