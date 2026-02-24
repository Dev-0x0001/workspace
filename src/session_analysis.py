from datetime import datetime
import json
from typing import List, Dict, Any
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisSession:
    def __init__(self, session_id: str, user_id: str, timestamp: datetime = None):
        self.session_id = session_id
        self.user_id = user_id
        self.timestamp = timestamp or datetime.now()
        self.interactions: List[Dict[str, Any]] = []
        self.analysis_results: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}

    def add_interaction(self, interaction: Dict[str, Any]) -> None:
        self.interactions.append(interaction)

    def analyze(self) -> Dict[str, Any]:
        # This is a simplified analysis
        if not self.interactions:
            return {'error': 'No interactions to analyze'}
        
        # In a real system, we would run ML models and analysis
        analysis = {
            'session_summary': f"Session with {len(self.interactions)} interactions",
            'timestamp_range': {
                'start': self.timestamp.isoformat(),
                'end': datetime.now().isoformat()
            },
            'user_id': self.user_id
        }
        
        # If there are interactions, add some detailed analysis
        if self.interactions:
            first_interaction = self.interactions[0]
            analysis['first_interaction'] = {
                'type': first_interaction.get('type'),
                'content': first_interaction.get('content')[:100] + '...' if first_interaction.get('content') else 'No content',
                'timestamp': first_interaction.get('timestamp', self.timestamp.isoformat())
            }
            
            # Simple sentiment analysis (this would be ML-based)
            sentiment = self._simple_sentiment_analysis()
            analysis['sentiment'] = sentiment
            
            # Intent distribution (this would use actual ML model)
            intent_distribution = self._intent_distribution()
            analysis['intent_distribution'] = intent_distribution
        
        self.analysis_results = analysis
        return analysis

    def _simple_sentiment_analysis(self) -> Dict[str, float]:
        # This is a very simple sentiment analysis - real systems would use ML models
        keywords = {
            'positive': ['happy', 'great', 'good', 'excellent', 'fine', 'wonderful'],
            'negative': ['sad', 'bad', 'awful', 'terrible', 'hate', 'frustrated'],
            'neutral': ['okay', 'fine', 'normal']
        }
        
        text = ' '.join([interaction.get('content', '') for interaction in self.interactions])
        text = text.lower()
        
        positive_count = sum(1 for word in keywords['positive'] if word in text)
        negative_count = sum(1 for word in keywords['negative'] if word in text)
        
        total = positive_count + negative_count
        if total == 0:
            return {'sentiment': 'neutral', 'confidence': 0.5}
        
        if positive_count > negative_count:
            return {'sentiment': 'positive', 'confidence': positive_count / total}
        elif negative_count > positive_count:
            return {'sentiment': 'negative', 'confidence': negative_count / total}
        else:
            return {'sentiment': 'neutral', 'confidence': 0.5}

    def _intent_distribution(self) -> Dict[str, Dict[str, float]]:
        # This would actually use the intent recognition model
        intents = [
            'information',
            'emotional_support',
            'instructional',
            'general'
        ]
        
        # In a real system, we would run the model on all interactions
        # This is just a demonstration
        distribution = {intent: 0.0 for intent in intents}
        
        if self.interactions:
            # Simple heuristic-based classification
            for interaction in self.interactions:
                content = interaction.get('content', '').lower()
                
                intent_score = {'information': 0, 'emotional_support': 0, 
                               'instructional': 0, 'general': 0}
                
                # Information intent keywords
                info_keywords = ['what', 'where', 'when', 'why', 'how', 'who',
                               'tell', 'explain', 'describe', 'definition',
                               'facts', 'data', 'statistics']
                info_count = sum(1 for word in info_keywords if word in content)
                
                # Emotional support keywords
                emotional_keywords = ['help', 'support', 'counsel', 'talk',
                                    'feel', 'emotion', 'stress', 'anxious',
                                    'depressed', 'frustrated', 'angry',
                                    'sad', 'happy', 'excited']
                emotional_count = sum(1 for word in emotional_keywords if word in content)
                
                # Instructional keywords
                instructional_keywords = ['teach', 'show', 'demonstrate',
                                        'tutorial', 'guide', 'example',
                                        'teaching', 'learn', 'instruction']
                instructional_count = sum(1 for word in instructional_keywords if word in content)
                
                # General keywords
                general_keywords = ['hi', 'hello', 'bye', 'goodbye', 'thanks',
                                  'thank', 'sorry', 'apologize', 'congratulate']
                general_count = sum(1 for word in general_keywords if word in content)
                
                # Score calculation
                max_count = max(info_count, emotional_count, instructional_count, general_count)
                
                if max_count == 0:
                    intent_score['general'] += 1
                else:
                    if info_count == max_count:
                        intent_score['information'] += 1
                    elif emotional_count == max_count:
                        intent_score['emotional_support'] += 1
                    elif instructional_count == max_count:
                        intent_score['instructional'] += 1
                    # general is already counted
            
            # Calculate distribution
            for intent in intents:
                count = intent_score.get(intent, 0)
                distribution[intent] = count / len(self.interactions)
        
        return distribution

    def to_dict(self) -> Dict[str, Any]:
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'interactions': self.interactions,
            'analysis_results': self.analysis_results,
            'metadata': self.metadata
        }

    @classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'AnalysisSession':
    session = cls(
        session_id=data['session_id'],
        user_id=data['user_id'],
        timestamp=datetime.fromisoformat(data['timestamp'])
    )
    session.interactions = data['interactions']
    session.analysis_results = data['analysis_results']
    session.metadata = data['metadata']
    return session