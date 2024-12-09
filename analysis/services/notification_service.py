from typing import Dict, List
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class NotificationService:
    def __init__(self):
        self.notification_types = {
            'signal': self._send_signal_notification,
            'alert': self._send_alert_notification,
            'risk': self._send_risk_notification,
            'system': self._send_system_notification
        }
    
    def send_notification(self, user: User, notification_type: str, data: Dict) -> None:
        """Envia uma notificação ao usuário"""
        if notification_type in self.notification_types:
            self.notification_types[notification_type](user, data)
    
    def _send_signal_notification(self, user: User, data: Dict) -> None:
        """Envia notificação de sinal de trading"""
        subject = f"Novo Sinal de Trading - {data['timeframe']}"
        message = f"""
        Novo sinal de trading detectado!
        
        Direção: {data['direction'].upper()}
        Preço de Entrada: ${data['entry_price']}
        Stop Loss: ${data['stop_loss']}
        Take Profit: ${data['take_profit']}
        Confiança: {data['confidence']}%
        
        Acesse a plataforma para mais detalhes.
        """
        
        self._send_email(user, subject, message)
    
    def _send_alert_notification(self, user: User, data: Dict) -> None:
        """Envia notificação de alerta de preço"""
        subject = "Alerta de Preço Atingido"
        message = f"""
        Alerta de preço atingido!
        
        Preço Atual: ${data['price']}
        Condição: {data['condition']}
        Alvo: ${data['target']}
        
        {data['message']}
        """
        
        self._send_email(user, subject, message)
    
    def _send_risk_notification(self, user: User, data: Dict) -> None:
        """Envia notificação de risco"""
        subject = f"Aviso de Risco - {data['risk_type']}"
        message = f"""
        Aviso de Risco Importante!
        
        Tipo: {data['risk_type']}
        Severidade: {data['severity']}
        
        {data['message']}
        
        Recomendações:
        {chr(10).join(f'- {r}' for r in data['recommendations'])}
        """
        
        self._send_email(user, subject, message)
    
    def _send_system_notification(self, user: User, data: Dict) -> None:
        """Envia notificação do sistema"""
        subject = "Notificação do Sistema"
        message = data['message']
        
        self._send_email(user, subject, message)
    
    def _send_email(self, user: User, subject: str, message: str) -> None:
        """Envia email ao usuário"""
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
        except Exception as e:
            print(f"Error sending email: {e}")