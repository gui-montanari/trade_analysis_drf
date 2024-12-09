from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    """Configurações personalizadas do usuário"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    max_risk_per_trade = models.FloatField(
        default=2.0,
        validators=[MinValueValidator(0.1), MaxValueValidator(10.0)],
        help_text="Risco máximo por operação (%)"
    )
    max_position_size = models.FloatField(
        default=10.0,
        validators=[MinValueValidator(1.0), MaxValueValidator(100.0)],
        help_text="Tamanho máximo da posição (%)"
    )
    preferred_leverage = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Alavancagem preferida"
    )
    notification_email = models.BooleanField(
        default=True,
        help_text="Receber notificações por email"
    )
    auto_update = models.BooleanField(
        default=True,
        help_text="Atualizar análises automaticamente"
    )
    update_interval = models.IntegerField(
        default=60,
        validators=[MinValueValidator(10), MaxValueValidator(3600)],
        help_text="Intervalo de atualização (segundos)"
    )

    class Meta:
        verbose_name = "Configuração do Usuário"
        verbose_name_plural = "Configurações dos Usuários"

    def __str__(self):
        return f"Configurações de {self.user.username}"

class TradingSignal(models.Model):
    """Sinais de trading gerados pelo sistema"""
    SIGNAL_TYPES = [
        ('futures', 'Futures'),
        ('day', 'Day Trading'),
        ('swing', 'Swing Trading'),
        ('position', 'Position Trading')
    ]
    
    DIRECTIONS = [
        ('buy', 'Compra'),
        ('sell', 'Venda'),
        ('neutral', 'Neutro')
    ]

    signal_type = models.CharField(max_length=10, choices=SIGNAL_TYPES)
    direction = models.CharField(max_length=10, choices=DIRECTIONS)
    entry_price = models.DecimalField(max_digits=20, decimal_places=8)
    stop_loss = models.DecimalField(max_digits=20, decimal_places=8)
    take_profit = models.DecimalField(max_digits=20, decimal_places=8)
    confidence = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    risk_reward = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    success = models.BooleanField(null=True, blank=True)
    
    # Metadados
    market_price = models.DecimalField(max_digits=20, decimal_places=8)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=2)
    change_24h = models.FloatField()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['signal_type', 'created_at']),
            models.Index(fields=['direction', 'is_active'])
        ]

    def __str__(self):
        return f"{self.signal_type} - {self.direction} at {self.entry_price}"

class Analysis(models.Model):
    """Análises técnicas e fundamentais"""
    ANALYSIS_TYPES = [
        ('futures', 'Futures'),
        ('day', 'Day Trading'),
        ('swing', 'Swing Trading'),
        ('position', 'Position Trading')
    ]

    analysis_type = models.CharField(max_length=10, choices=ANALYSIS_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    
    # Indicadores técnicos
    rsi = models.FloatField()
    macd = models.FloatField()
    signal_line = models.FloatField()
    upper_band = models.FloatField()
    lower_band = models.FloatField()
    
    # Análise de tendência
    trend = models.CharField(max_length=20)
    trend_strength = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Métricas de mercado
    volume = models.DecimalField(max_digits=20, decimal_places=2)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2)
    dominance = models.FloatField()
    
    # Resultado da análise
    recommendation = models.TextField()
    confidence = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['analysis_type', 'timestamp'])
        ]
        verbose_name = "Análise"
        verbose_name_plural = "Análises"

    def __str__(self):
        return f"{self.analysis_type} Analysis at {self.timestamp}"

class Alert(models.Model):
    """Alertas de preço e condições de mercado"""
    ALERT_TYPES = [
        ('price', 'Preço'),
        ('indicator', 'Indicador'),
        ('volume', 'Volume'),
        ('trend', 'Tendência')
    ]
    
    CONDITIONS = [
        ('above', 'Acima'),
        ('below', 'Abaixo'),
        ('crosses_up', 'Cruza para Cima'),
        ('crosses_down', 'Cruza para Baixo')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES)
    condition = models.CharField(max_length=12, choices=CONDITIONS)
    target_value = models.DecimalField(max_digits=20, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    triggered = models.BooleanField(default=False)
    triggered_at = models.DateTimeField(null=True, blank=True)
    notification_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'alert_type']),
            models.Index(fields=['is_active', 'triggered'])
        ]

    def __str__(self):
        return f"{self.alert_type} Alert for {self.user.username}"

class AnalysisHistory(models.Model):
    """Histórico de análises realizadas"""
    signal = models.ForeignKey(TradingSignal, on_delete=models.CASCADE)
    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    success_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    profit_loss = models.FloatField(null=True, blank=True)
    max_drawdown = models.FloatField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Histórico de Análise"
        verbose_name_plural = "Histórico de Análises"

    def __str__(self):
        return f"History for {self.signal} at {self.created_at}"

class UserNotification(models.Model):
    """Notificações do usuário"""
    NOTIFICATION_TYPES = [
        ('signal', 'Sinal de Trading'),
        ('alert', 'Alerta'),
        ('risk', 'Risco'),
        ('system', 'Sistema')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'notification_type']),
            models.Index(fields=['read', 'created_at'])
        ]

    def __str__(self):
        return f"{self.notification_type} for {self.user.username}"
    

class TradingNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('signal', 'Sinal de Trading'),
        ('alert', 'Alerta de Preço'),
        ('risk', 'Aviso de Risco'),
    ]

    TRADING_TYPES = [
        ('futures', 'Futures'),
        ('day', 'Day Trading'),
        ('swing', 'Swing'),
        ('position', 'Position'),
    ]

    SIGNAL_TYPES = [
        ('buy', 'Compra'),
        ('sell', 'Venda'),
        ('neutral', 'Neutro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    trading_type = models.CharField(max_length=10, choices=TRADING_TYPES)
    signal_type = models.CharField(max_length=10, choices=SIGNAL_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    importance = models.IntegerField(default=1)  # 1-Normal, 2-Important, 3-Critical

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['notification_type', 'trading_type']),
        ]

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"