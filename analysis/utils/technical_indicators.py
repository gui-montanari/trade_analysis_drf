import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime

class TechnicalIndicators:
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
        """Calcula o RSI (Relative Strength Index)"""
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum()/period
        down = -seed[seed < 0].sum()/period
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100./(1. + rs)

        for i in range(period, len(prices)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(period-1) + upval)/period
            down = (down*(period-1) + downval)/period
            rs = up/down
            rsi[i] = 100. - 100./(1. + rs)

        return rsi

    @staticmethod
    def calculate_macd(prices: List[float], 
                      fast_period: int = 12, 
                      slow_period: int = 26, 
                      signal_period: int = 9) -> Tuple[List[float], List[float]]:
        """Calcula MACD (Moving Average Convergence Divergence)"""
        # Calcular EMA rápida e lenta
        fast_ema = TechnicalIndicators.calculate_ema(prices, fast_period)
        slow_ema = TechnicalIndicators.calculate_ema(prices, slow_period)
        
        # Calcular linha MACD
        macd_line = [f - s for f, s in zip(fast_ema, slow_ema)]
        
        # Calcular linha de sinal
        signal_line = TechnicalIndicators.calculate_ema(macd_line, signal_period)
        
        return macd_line, signal_line

    @staticmethod
    def calculate_ema(prices: List[float], period: int) -> List[float]:
        """Calcula EMA (Exponential Moving Average)"""
        multiplier = 2 / (period + 1)
        ema = [prices[0]]  # Primeiro valor é o mesmo do preço
        
        for price in prices[1:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
            
        return ema

    @staticmethod
    def calculate_bollinger_bands(prices: List[float], 
                                period: int = 20, 
                                num_std: float = 2) -> Tuple[List[float], List[float], List[float]]:
        """Calcula Bandas de Bollinger"""
        sma = TechnicalIndicators.calculate_sma(prices, period)
        std = TechnicalIndicators.calculate_rolling_std(prices, period)
        
        upper_band = [sma[i] + (std[i] * num_std) for i in range(len(sma))]
        lower_band = [sma[i] - (std[i] * num_std) for i in range(len(sma))]
        
        return upper_band, sma, lower_band

    @staticmethod
    def calculate_sma(prices: List[float], period: int) -> List[float]:
        """Calcula SMA (Simple Moving Average)"""
        if len(prices) < period:
            return prices
            
        sma = []
        for i in range(len(prices)):
            if i < period - 1:
                sma.append(prices[i])
            else:
                sma.append(sum(prices[i-period+1:i+1]) / period)
                
        return sma

    @staticmethod
    def calculate_rolling_std(prices: List[float], period: int) -> List[float]:
        """Calcula desvio padrão móvel"""
        std = []
        for i in range(len(prices)):
            if i < period - 1:
                std.append(0)
            else:
                window = prices[i-period+1:i+1]
                std.append(np.std(window))
                
        return std

    @staticmethod
    def find_support_resistance(prices: List[float], 
                              window: int = 20, 
                              threshold: float = 0.02) -> Dict[str, List[float]]:
        """Encontra níveis de suporte e resistência"""
        supports = []
        resistances = []
        
        for i in range(window, len(prices)-window):
            # Check for support
            if all(prices[i] <= prices[j] for j in range(i-window, i+window+1)):
                supports.append(prices[i])
                
            # Check for resistance
            if all(prices[i] >= prices[j] for j in range(i-window, i+window+1)):
                resistances.append(prices[i])
                
        return {
            'supports': supports,
            'resistances': resistances
        }