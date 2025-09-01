# Bitcoin Prediction Dashboard

A Flask web application that provides Bitcoin buy/sell predictions based on technical analysis and sentiment analysis.

## Features

- Real-time Bitcoin price tracking
- Technical analysis (RSI, MACD, Bollinger Bands, Moving Averages)
- Sentiment analysis from news and social media
- Interactive price charts
- Responsive web interface
- Buy/Sell/Neutral predictions with confidence scores

## Installation

1. **Clone or download the project files**

2. **Create a virtual environment:**
```bash
python -m venv venv
```

3. **Activate the virtual environment:**

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Set up environment variables:**
- Replace API keys with your actual keys (optional for basic functionality)

1. **Run the application:**
```bash
python app.py
```

Or alternatively:
```bash
python run.py
```

7. **Open your browser and navigate to:**
```
http://localhost:5000
```

## Project Structure

```
bitcoin_predictor/
├── app.py                 # Main Flask application
├── run.py                 # Alternative app runner
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md             # This file
├── models/               # Analysis modules
│   ├── __init__.py
│   ├── technical_analysis.py
│   ├── sentiment_analysis.py
│   └── prediction_model.py
├── templates/            # HTML templates
│   └── dashboard.html
└── static/              # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── dashboard.js
```

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/price` - Current Bitcoin price
- `GET /api/prediction` - Trading prediction
- `GET /api/chart-data` - Price chart data

## Customization

### Adding Real Data Sources

1. **News API Integration:**
   - Sign up for NewsAPI at https://newsapi.org/
   - Replace `NEWS_API_KEY` in `.env`
   - Modify `sentiment_analysis.py` to use real news data

2. **Social Media Integration:**
   - Add Twitter API credentials
   - Add Reddit API credentials
   - Implement real social sentiment analysis

3. **Enhanced Technical Analysis:**
   - Install TA-Lib: `pip install TA-Lib`
   - Add more technical indicators
   - Implement backtesting functionality

### Deployment

For production deployment:

1. **Set Flask environment to production:**
```bash
export FLASK_ENV=production
```

2. **Use a production WSGI server:**
```bash
pip install gunicorn
gunicorn app:app
```

3. **Deploy to platforms like:**
   - Heroku
   - DigitalOcean
   - AWS
   - Google Cloud Platform

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Disclaimer

This application is for educational purposes only. Do not use it for actual trading decisions without proper research and risk management. Cryptocurrency trading involves substantial risk.

## License

MIT License - feel free to modify and distribute as needed.
