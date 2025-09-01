import requests
import random
from datetime import datetime, timedelta

class SentimentAnalysis:
    def __init__(self):
        self.news_sources = [
            "Bitcoin ETFs see record inflows amid institutional adoption",
            "Major corporation announces Bitcoin treasury strategy",
            "Regulatory clarity improves crypto market outlook",
            "Cryptocurrency adoption accelerates in emerging markets",
            "New Bitcoin mining facility goes online with green energy",
            "Financial institutions increase Bitcoin allocations"
        ]
    
    def analyze(self):
        """Perform sentiment analysis from various sources"""
        try:
            # In a real implementation, you would:
            # 1. Fetch news from crypto news APIs
            # 2. Analyze social media sentiment
            # 3. Check fear & greed index
            # 4. Process market sentiment indicators
            
            news_sentiment = self.analyze_news_sentiment()
            social_sentiment = self.analyze_social_sentiment()
            market_sentiment = self.analyze_market_sentiment()
            
            # Combine sentiments
            overall_score = (news_sentiment + social_sentiment + market_sentiment) / 3
            
            return {
                'score': max(0, min(100, overall_score)),
                'news_sentiment': news_sentiment,
                'social_sentiment': social_sentiment,
                'market_sentiment': market_sentiment,
                'news_items': self.get_recent_news()
            }
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return self.get_demo_sentiment_analysis()
    
    def analyze_news_sentiment(self):
        """Analyze news sentiment"""
        # Demo implementation - in real app, use NewsAPI or similar
        return random.randint(60, 90)
    
    def analyze_social_sentiment(self):
        """Analyze social media sentiment"""
        # Demo implementation - in real app, analyze Twitter/Reddit
        return random.randint(55, 85)
    
    def analyze_market_sentiment(self):
        """Analyze overall market sentiment"""
        # Demo implementation - in real app, use Fear & Greed Index
        return random.randint(50, 80)
    
    def get_recent_news(self):
        """Get recent news items with sentiment"""
        news_items = []
        for i, headline in enumerate(self.news_sources[:3]):
            sentiment_score = random.uniform(0.3, 0.9)
            sentiment = "Positive" if sentiment_score > 0.1 else ("Negative" if sentiment_score < -0.1 else "Neutral")
            sentiment_class = "bullish" if sentiment == "Positive" else ("bearish" if sentiment == "Negative" else "neutral-signal")
            
            news_items.append({
                'title': headline,
                'sentiment': sentiment,
                'sentiment_class': sentiment_class,
                'time_ago': f"{random.randint(1, 8)} hours ago"
            })
        
        return news_items
    
    def get_demo_sentiment_analysis(self):
        """Return demo sentiment analysis"""
        return {
            'score': 75,
            'news_sentiment': 80,
            'social_sentiment': 70,
            'market_sentiment': 75,
            'news_items': self.get_recent_news()
        }