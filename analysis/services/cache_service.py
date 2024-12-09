from typing import Any, Optional
from datetime import datetime, timedelta
from django.core.cache import cache
from ..utils.config import CACHE_CONFIG

class CacheService:
    def __init__(self):
        self.enabled = CACHE_CONFIG['enabled']
        self.timeouts = CACHE_CONFIG['timeout']
    
    def get_market_data(self, key: str) -> Optional[Any]:
        """Obtém dados de mercado do cache"""
        if not self.enabled:
            return None
            
        cache_key = f"market_data_{key}"
        return cache.get(cache_key)
    
    def set_market_data(self, key: str, data: Any) -> None:
        """Armazena dados de mercado no cache"""
        if not self.enabled:
            return
            
        cache_key = f"market_data_{key}"
        cache.set(cache_key, data, self.timeouts['market_data'])
    
    def get_technical_data(self, key: str) -> Optional[Any]:
        """Obtém dados técnicos do cache"""
        if not self.enabled:
            return None
            
        cache_key = f"technical_data_{key}"
        return cache.get(cache_key)
    
    def set_technical_data(self, key: str, data: Any) -> None:
        """Armazena dados técnicos no cache"""
        if not self.enabled:
            return
            
        cache_key = f"technical_data_{key}"
        cache.set(cache_key, data, self.timeouts['technical_data'])
    
    def get_analysis(self, analysis_type: str, key: str) -> Optional[Any]:
        """Obtém análise do cache"""
        if not self.enabled:
            return None
            
        cache_key = f"analysis_{analysis_type}_{key}"
        return cache.get(cache_key)
    
    def set_analysis(self, analysis_type: str, key: str, data: Any) -> None:
        """Armazena análise no cache"""
        if not self.enabled:
            return
            
        cache_key = f"analysis_{analysis_type}_{key}"
        timeout = self.timeouts.get(analysis_type, 300)  # 5 minutos default
        cache.set(cache_key, data, timeout)
    
    def invalidate_market_data(self) -> None:
        """Invalida cache de dados de mercado"""
        if not self.enabled:
            return
            
        keys = cache.keys("market_data_*")
        cache.delete_many(keys)
    
    def invalidate_technical_data(self) -> None:
        """Invalida cache de dados técnicos"""
        if not self.enabled:
            return
            
        keys = cache.keys("technical_data_*")
        cache.delete_many(keys)
    
    def invalidate_analysis(self, analysis_type: Optional[str] = None) -> None:
        """Invalida cache de análises"""
        if not self.enabled:
            return
            
        if analysis_type:
            keys = cache.keys(f"analysis_{analysis_type}_*")
        else:
            keys = cache.keys("analysis_*")
            
        cache.delete_many(keys)
    
    def clear_all(self) -> None:
        """Limpa todo o cache"""
        if not self.enabled:
            return
            
        cache.clear()