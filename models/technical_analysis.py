import pandas as pd
import numpy as np
from datetime import datetime
import random

class TechnicalAnalysis:
    def __init__(self):
        pass
    
    def analyze(self, price_data):
        """Perform comprehensive technical analysis"""
        try:
            prices = pd.Series(price_data['prices'])
            volumes = pd.Series(price_data['volumes'])
            
            # Calculate technical indicators
            rsi = self.calculate_rsi(prices)
            macd_line, macd_signal = self.calculate_macd(prices)
            bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(prices)
            sma_20 = self.calculate_sma(prices, 20)
            sma_50 = self.calculate_sma(prices, 50)
            
            # Volume analysis
            volume_trend = self.analyze_volume(volumes)
            
            # Generate signals
            rsi_signal = self.interpret_rsi(rsi.iloc[-1])
            macd_signal_value = self.interpret_macd(macd_line.iloc[-1], macd_signal.iloc[-1])
            bb_signal = self.interpret_bollinger_bands(prices.iloc[-1], bb_upper.iloc[-1], bb_lower.iloc[-1])
            ma_signal = self.interpret_moving_averages(prices.iloc[-1], sma_20.iloc[-1], sma_50.iloc[-1])
            
            # Calculate overall technical score
            signals = [rsi_signal, macd_signal_value, bb_signal, ma_signal, volume_trend]
            overall_score = sum(signals) / len(signals) * 20 + 50  # Scale to 0-100
            
            return {
                'overall_score': max(0, min(100, overall_score)),
                'indicators': {
                    'rsi': {
                        'value': round(rsi.iloc[-1], 1),
                        'signal': self.signal_to_text(rsi_signal),
                        'signal_class': self.signal_to_class(rsi_signal)
                    },
                    'macd': {
                        'value': round(macd_line.iloc[-1] - macd_signal.iloc[-1], 1),
                        'signal': self.signal_to_text(macd_signal_value),
                        'signal_class': self.signal_to_class(macd_signal_value)
                    },
                    'bollinger_bands': {
                        'value': 'Middle' if abs(prices.iloc[-1] - bb_middle.iloc[-1]) < abs(prices.iloc[-1] - bb_upper.iloc[-1]) else ('Upper' if prices.iloc[-1] > bb_middle.iloc[-1] else 'Lower'),
                        'signal': self.signal_to_text(bb_signal),
                        'signal_class': self.signal_to_class(bb_signal)
                    },
                    'volume': {
                        'value': 'High' if volume_trend > 0 else 'Low',
                        'signal': self.signal_to_text(volume_trend),
                        'signal_class': self.signal_to_class(volume_trend)
                    }
                }
            }
        except Exception as e:
            print(f"Technical analysis error: {e}")
            return self.get_demo_technical_analysis()
    
    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        macd_signal = macd_line.ewm(span=signal).mean()
        return macd_line, macd_signal
    
    def calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        return upper_band, sma, lower_band
    
    def calculate_sma(self, prices, period):
        """Calculate Simple Moving Average"""
        return prices.rolling(window=period).mean()
    
    def analyze_volume(self, volumes):
        """Analyze volume trend"""
        if len(volumes) < 10:
            return 0
        recent_avg = volumes.tail(5).mean()
        historical_avg = volumes.head(len(volumes)-5).mean()
        return 1 if recent_avg > historical_avg * 1.2 else (-1 if recent_avg < historical_avg * 0.8 else 0)
    
    def interpret_rsi(self, rsi_value):
        """Interpret RSI value"""
        if rsi_value > 70:
            return -1  # Overbought
        elif rsi_value < 30:
            return 1   # Oversold
        else:
            return 0   # Neutral
    
    def interpret_macd(self, macd_line, macd_signal):
        """Interpret MACD"""
        return 1 if macd_line > macd_signal else -1
    
    def interpret_bollinger_bands(self, price, upper, lower):
        """Interpret Bollinger Bands"""
        if price > upper:
            return -1  # Overbought
        elif price < lower:
            return 1   # Oversold
        else:
            return 0   # Neutral
    
    def interpret_moving_averages(self, price, sma_20, sma_50):
        """Interpret Moving Averages"""
        if price > sma_20 > sma_50:
            return 1   # Bullish
        elif price < sma_20 < sma_50:
            return -1  # Bearish
        else:
            return 0   # Neutral
    
    def signal_to_text(self, signal):
        """Convert signal to text"""
        if signal > 0:
            return "Bullish"
        elif signal < 0:
            return "Bearish"
        else:
            return "Neutral"
    
    def signal_to_class(self, signal):
        """Convert signal to CSS class"""
        if signal > 0:
            return "bullish"
        elif signal < 0:
            return "bearish"
        else:
            return "neutral-signal"
    
    def get_demo_technical_analysis(self):
        """Return demo data when API fails"""
        return {
            'overall_score': random.randint(60, 80),
            'indicators': {
                'rsi': {'value': round(random.uniform(40, 70), 1), 'signal': 'Neutral', 'signal_class': 'neutral-signal'},
                'macd': {'value': round(random.uniform(-500, 500), 1), 'signal': 'Bullish', 'signal_class': 'bullish'},
                'bollinger_bands': {'value': 'Middle', 'signal': 'Neutral', 'signal_class': 'neutral-signal'},
                'volume': {'value': 'High', 'signal': 'Bullish', 'signal_class': 'bullish'}
            }
        }
