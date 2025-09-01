import random

class PredictionModel:
    def __init__(self):
        pass
    
    def predict(self, technical_analysis, sentiment_analysis):
        """Generate prediction based on technical and sentiment analysis"""
        try:
            # Combine technical and sentiment scores
            technical_score = technical_analysis['overall_score']
            sentiment_score = sentiment_analysis['score']
            
            # Weighted combination (60% technical, 40% sentiment)
            combined_score = (technical_score * 0.6) + (sentiment_score * 0.4)
            
            # Generate confidence based on agreement between indicators
            confidence = self.calculate_confidence(technical_score, sentiment_score)
            
            # Determine signal
            signal = self.determine_signal(combined_score)
            
            return {
                'signal': signal,
                'confidence': confidence,
                'combined_score': combined_score,
                'technical_weight': 0.6,
                'sentiment_weight': 0.4
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return {
                'signal': 'neutral',
                'confidence': 50,
                'combined_score': 50,
                'technical_weight': 0.6,
                'sentiment_weight': 0.4
            }
    
    def determine_signal(self, score):
        """Determine buy/sell signal based on combined score"""
        if score >= 80:
            return 'strong_buy'
        elif score >= 65:
            return 'buy'
        elif score >= 35:
            return 'neutral'
        elif score >= 20:
            return 'sell'
        else:
            return 'strong_sell'
    
    def calculate_confidence(self, technical_score, sentiment_score):
        """Calculate confidence based on agreement between scores"""
        difference = abs(technical_score - sentiment_score)
        agreement = 100 - difference
        
        # Base confidence on agreement and absolute scores
        avg_score = (technical_score + sentiment_score) / 2
        confidence = (agreement * 0.4) + (avg_score * 0.6)
        
        return max(50, min(95, int(confidence)))