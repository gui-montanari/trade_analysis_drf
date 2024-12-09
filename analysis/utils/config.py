from typing import Dict

# Configurações de Análise
ANALYSIS_CONFIG = {
    'futures': {
        'max_leverage': 10,
        'min_risk_reward': 2.0,
        'max_position_size': 0.1,
        'update_interval': 10,  # segundos
        'indicators': {
            'rsi_period': 14,
            'macd_fast': 12,
            'macd_slow': 26,
            'macd_signal': 9,
            'bollinger_period': 20,
            'bollinger_std': 2
        }
    },
    'day_trading': {
        'min_risk_reward': 1.5,
        'max_position_size': 0.05,
        'update_interval': 60,  # segundos
    },
    'swing': {
        'min_risk_reward': 2.5,
        'max_position_size': 0.15,
        'min_holding_period': '3d',
        'max_holding_period': '30d'
    },
    'position': {
        'min_risk_reward': 3.0,
        'max_allocation': 0.25,
        'min_holding_period': '90d'
    }
}

# Configurações de Risco
RISK_CONFIG = {
    'max_portfolio_risk': 0.02,  # 2% máximo risco por trade
    'max_daily_risk': 0.06,      # 6% máximo risco diário
    'max_correlation': 0.7,      # Máxima correlação permitida
    'leverage_tiers': {
        'low_risk': 3,
        'medium_risk': 5,
        'high_risk': 10
    }
}

# Configurações de Mercado
MARKET_CONFIG = {
    'default_pair': 'BTC/USDT',
    'timeframes': {
        'futures': ['1m', '5m', '15m', '1h'],
        'day': ['5m', '15m', '1h', '4h'],
        'swing': ['4h', '1d', '1w'],
        'position': ['1d', '1w', '1M']
    },
    'api': {
        'base_url': 'https://api.coingecko.com/api/v3',
        'timeout': 30,
        'retry_attempts': 3
    }
}

# Configurações de Cache
CACHE_CONFIG = {
    'enabled': True,
    'timeout': {
        'market_data': 60,       # 1 minuto
        'technical_data': 300,   # 5 minutos
        'fundamental_data': 3600 # 1 hora
    }
}