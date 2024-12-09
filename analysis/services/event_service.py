from typing import Dict, List, Optional
from datetime import datetime
from django.db import transaction
from django.contrib.auth.models import User

class EventService:
    def __init__(self):
        self.event_types = {
            'signal': 'Trading Signal',
            'alert': 'Price Alert',
            'risk': 'Risk Warning',
            'system': 'System Event'
        }
    
    def log_signal(self, user: User, signal_data: Dict) -> None:
        """Registra um sinal de trading"""
        try:
            with transaction.atomic():
                event_data = {
                    'type': 'signal',
                    'user': user,
                    'timestamp': datetime.now(),
                    'data': {
                        'direction': signal_data.get('direction'),
                        'entry_price': signal_data.get('entry_price'),
                        'stop_loss': signal_data.get('stop_loss'),
                        'take_profit': signal_data.get('take_profit'),
                        'timeframe': signal_data.get('timeframe'),
                        'confidence': signal_data.get('confidence')
                    }
                }
                # Aqui você pode salvar em um modelo Django ou outro storage
                self._save_event(event_data)
        except Exception as e:
            print(f"Error logging signal: {e}")
    
    def log_alert(self, user: User, alert_data: Dict) -> None:
        """Registra um alerta de preço"""
        try:
            with transaction.atomic():
                event_data = {
                    'type': 'alert',
                    'user': user,
                    'timestamp': datetime.now(),
                    'data': {
                        'price': alert_data.get('price'),
                        'condition': alert_data.get('condition'),
                        'target': alert_data.get('target'),
                        'message': alert_data.get('message')
                    }
                }
                self._save_event(event_data)
        except Exception as e:
            print(f"Error logging alert: {e}")
    
    def log_risk_warning(self, user: User, warning_data: Dict) -> None:
        """Registra um aviso de risco"""
        try:
            with transaction.atomic():
                event_data = {
                    'type': 'risk',
                    'user': user,
                    'timestamp': datetime.now(),
                    'data': {
                        'risk_type': warning_data.get('risk_type'),
                        'severity': warning_data.get('severity'),
                        'message': warning_data.get('message'),
                        'recommendations': warning_data.get('recommendations', [])
                    }
                }
                self._save_event(event_data)
        except Exception as e:
            print(f"Error logging risk warning: {e}")
    
    def get_user_events(self, user: User, 
                       event_type: Optional[str] = None, 
                       limit: int = 50) -> List[Dict]:
        """Obtém eventos do usuário"""
        try:
            # Aqui você implementaria a lógica para buscar do seu storage
            events = []  # Buscar do banco de dados
            
            if event_type:
                events = [e for e in events if e['type'] == event_type]
                
            return sorted(events, 
                         key=lambda x: x['timestamp'], 
                         reverse=True)[:limit]
        except Exception as e:
            print(f"Error getting user events: {e}")
            return []
    
    def _save_event(self, event_data: Dict) -> None:
        """Salva um evento no storage"""
        # Aqui você implementaria a lógica de salvar no seu storage
        pass