import requests
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import numpy as np
from django.core.cache import cache

class MarketDataService:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.cache_timeout = 60  # 60 segundos
        
    def get_current_data(self) -> Dict:
        """Obtém dados atuais do mercado"""
        cache_key = 'market_data_current'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            # Dados do Bitcoin
            btc_data = self._fetch_bitcoin_data()
            
            # Dados globais
            global_data = self._fetch_global_data()
            
            market_data = {
                'price': btc_data['current_price']['usd'],
                'change_24h': btc_data['price_change_percentage_24h'],
                'volume_24h': btc_data['total_volume']['usd'],
                'market_cap': btc_data['market_cap']['usd'],
                'high_24h': btc_data['high_24h']['usd'],
                'low_24h': btc_data['low_24h']['usd'],
                'btc_dominance': global_data['btc_dominance'],
                'dominance_change': self._calculate_dominance_change(),
                'timestamp': datetime.now().isoformat()
            }
            
            cache.set(cache_key, market_data, self.cache_timeout)
            return market_data
            
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return self._get_default_data()

    def get_historical_data(self, days: int = 30) -> Dict:
        """Obtém dados históricos"""
        cache_key = f'market_data_historical_{days}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            url = f"{self.base_url}/coins/bitcoin/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            historical_data = {
                'prices': [price[1] for price in data['prices']],
                'volumes': [volume[1] for volume in data['total_volumes']],
                'market_caps': [cap[1] for cap in data['market_caps']],
                'timestamps': [datetime.fromtimestamp(price[0]/1000) for price in data['prices']]
            }
            
            cache.set(cache_key, historical_data, self.cache_timeout * 5)
            return historical_data
            
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return self._get_default_historical_data()

    def get_onchain_data(self) -> Dict:
        """Obtém dados on-chain"""
        try:
            # Aqui você pode integrar com APIs como Glassnode ou outras fontes
            # Por enquanto retornamos dados simulados
            return {
                'active_addresses': 1_000_000,
                'network_hash_rate': '150 EH/s',
                'average_transaction_fee': 5.5,
                'mempool_size': 15_000
            }
        except Exception as e:
            print(f"Error fetching onchain data: {e}")
            return {}

    def _fetch_bitcoin_data(self) -> Dict:
        """Busca dados específicos do Bitcoin"""
        url = f"{self.base_url}/coins/bitcoin"
        params = {
            'localization': False,
            'tickers': False,
            'community_data': False,
            'developer_data': False
        }
        
        response = requests.get(url, params=params)
        return response.json()['market_data']

    def _fetch_global_data(self) -> Dict:
        """Busca dados globais do mercado"""
        url = f"{self.base_url}/global"
        response = requests.get(url)
        data = response.json()['data']
        
        return {
            'btc_dominance': data['market_cap_percentage']['btc'],
            'total_market_cap': data['total_market_cap']['usd'],
            'total_volume': data['total_volume']['usd']
        }

    def _calculate_dominance_change(self) -> float:
        """Calcula mudança na dominância do BTC"""
        try:
            historical = self.get_historical_data(days=2)
            if historical and 'market_caps' in historical:
                old_dom = historical['market_caps'][0]
                new_dom = historical['market_caps'][-1]
                return ((new_dom - old_dom) / old_dom) * 100
            return 0.0
        except:
            return 0.0

    def _get_default_data(self) -> Dict:
        """Retorna dados padrão em caso de erro"""
        return {
            'price': 0.0,
            'change_24h': 0.0,
            'volume_24h': 0.0,
            'market_cap': 0.0,
            'high_24h': 0.0,
            'low_24h': 0.0,
            'btc_dominance': 0.0,
            'dominance_change': 0.0,
            'timestamp': datetime.now().isoformat()
        }

    def _get_default_historical_data(self) -> Dict:
        """Retorna dados históricos padrão em caso de erro"""
        return {
            'prices': [],
            'volumes': [],
            'market_caps': [],
            'timestamps': []
        }