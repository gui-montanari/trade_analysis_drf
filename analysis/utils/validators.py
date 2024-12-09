from typing import Dict, List, Optional, Union
from datetime import datetime

class AnalysisValidator:
    @staticmethod
    def validate_market_data(data: Dict) -> bool:
        """Valida dados de mercado"""
        required_fields = ['price', 'volume_24h', 'change_24h', 'market_cap']
        
        try:
            # Verificar campos obrigatórios
            if not all(field in data for field in required_fields):
                return False
                
            # Verificar valores válidos
            if not all(isinstance(data[field], (int, float)) for field in required_fields):
                return False
                
            # Verificar valores positivos
            if not all(data[field] >= 0 for field in ['price', 'volume_24h', 'market_cap']):
                return False
                
            return True
            
        except Exception:
            return False

    @staticmethod
    def validate_technical_indicators(indicators: Dict) -> bool:
        """Valida indicadores técnicos"""
        required_indicators = ['rsi', 'macd', 'bollinger_bands']
        
        try:
            # Verificar presença dos indicadores
            if not all(ind in indicators for ind in required_indicators):
                return False
                
            # Validar RSI
            if not 0 <= indicators['rsi'] <= 100:
                return False
                
            # Validar Bandas de Bollinger
            if 'bollinger_bands' in indicators:
                bb = indicators['bollinger_bands']
                if not (len(bb) == 3 and all(isinstance(band, list) for band in bb)):
                    return False
                    
            return True
            
        except Exception:
            return False

    @staticmethod
    def validate_risk_metrics(metrics: Dict) -> bool:
        """Valida métricas de risco"""
        required_metrics = [
            'risk_reward_ratio',
            'position_size',
            'max_risk'
        ]
        
        try:
            # Verificar campos obrigatórios
            if not all(metric in metrics for metric in required_metrics):
                return False
                
            # Verificar valores válidos
            if metrics['risk_reward_ratio'] <= 0:
                return False
                
            if not (0 < metrics['position_size'] <= 100):
                return False
                
            if metrics['max_risk'] < 0:
                return False
                
            return True
            
        except Exception:
            return False

    @staticmethod
    def validate_trading_signal(signal: Dict) -> bool:
        """Valida sinal de trading"""
        required_fields = [
            'direction',
            'entry_price',
            'stop_loss',
            'take_profit'
        ]
        
        try:
            # Verificar campos obrigatórios
            if not all(field in signal for field in required_fields):
                return False
                
            # Verificar direção válida
            if signal['direction'] not in ['buy', 'sell', 'neutral']:
                return False
                
            # Verificar preços válidos
            prices = [signal['entry_price'], signal['stop_loss'], signal['take_profit']]
            if not all(isinstance(p, (int, float)) and p > 0 for p in prices):
                return False
                
            return True
            
        except Exception:
            return False