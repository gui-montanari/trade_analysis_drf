from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from ..models import TradingNotification

class NotificationService:
    @staticmethod
    def create_signal_notification(user: User, analysis_data: dict, trading_type: str):
        """Criar notificação baseada em sinais de trading"""
        signal_type = analysis_data.get('signal_type', 'neutral')
        confidence = analysis_data.get('confidence', 0)

        # Só criar notificação se o sinal for forte o suficiente
        if confidence >= 75:
            importance = 3  # Critical
        elif confidence >= 65:
            importance = 2  # Important
        else:
            return None

        message = (
            f"Sinal de {analysis_data.get('signal', 'NEUTRO')} detectado!\n"
            f"Preço: ${analysis_data.get('entry_price', 0):,.2f}\n"
            f"Stop Loss: ${analysis_data.get('stop_loss', 0):,.2f}\n"
            f"Take Profit: ${analysis_data.get('take_profit', 0):,.2f}\n"
            f"Confiança: {confidence}%"
        )

        return TradingNotification.objects.create(
            user=user,
            notification_type='signal',
            trading_type=trading_type,
            signal_type=signal_type,
            title=f"Novo sinal de {analysis_data.get('signal', 'NEUTRO')} - {trading_type.upper()}",
            message=message,
            price=analysis_data.get('entry_price', 0),
            importance=importance
        )

    @staticmethod
    def create_risk_notification(user: User, risk_data: dict, trading_type: str):
        """Criar notificação de risco"""
        if risk_data.get('risk_score', 0) >= 7:
            message = (
                f"Alto risco detectado!\n"
                f"Score de Risco: {risk_data.get('risk_score')}/10\n"
                f"Risco Máximo: {risk_data.get('max_risk')}%\n"
                f"Recomendação: {risk_data.get('recommendations', ['Reduzir exposição'])[0]}"
            )

            return TradingNotification.objects.create(
                user=user,
                notification_type='risk',
                trading_type=trading_type,
                signal_type='neutral',
                title=f"Aviso de Risco - {trading_type.upper()}",
                message=message,
                price=risk_data.get('current_price', 0),
                importance=3  # Critical
            )

    @staticmethod
    def get_user_notifications(user: User, limit: int = 10, unread_only: bool = False):
        """Obter notificações do usuário"""
        query = Q(user=user)
        if unread_only:
            query &= Q(read=False)

        return TradingNotification.objects.filter(query)[:limit]

    @staticmethod
    def mark_as_read(notification_id: int, user: User) -> bool:
        """Marcar notificação como lida"""
        try:
            notification = TradingNotification.objects.get(id=notification_id, user=user)
            notification.read = True
            notification.read_at = timezone.now()
            notification.save()
            return True
        except TradingNotification.DoesNotExist:
            return False

    @staticmethod
    def mark_all_as_read(user: User):
        """Marcar todas as notificações do usuário como lidas"""
        TradingNotification.objects.filter(user=user, read=False).update(
            read=True,
            read_at=timezone.now()
        )

    @staticmethod
    def get_unread_count(user: User) -> int:
        """Obter contagem de notificações não lidas"""
        return TradingNotification.objects.filter(user=user, read=False).count()