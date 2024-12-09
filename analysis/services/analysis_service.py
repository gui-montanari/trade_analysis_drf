from typing import Dict, List, Optional, Tuple, Union, Any
import numpy as np
from datetime import datetime
from django.conf import settings
from django.core.cache import cache

class AnalysisService:
    def __init__(self):
        self.technical_threshold = 65  # Threshold para sinais técnicos
        self.min_risk_reward = 2.0     # Mínimo risco/retorno
        self.max_leverage = 10         # Alavancagem máxima
        
    def analyze_futures(self, market_data: Dict) -> Dict:
        """Análise para Futures Trading"""
        try:
            # Calcular indicadores técnicos
            indicators = self._calculate_technical_indicators(market_data)
            
            # Determinar sinal com base nos indicadores
            signal_data = self._generate_futures_signal(indicators)
            
            # Calcular níveis de entrada/saída
            levels = self._calculate_futures_levels(market_data['price'], signal_data['signal'])
            
            # Calcular métricas adicionais
            metrics = self._calculate_futures_metrics(market_data)
            
            return {
                'signal': signal_data['signal'],
                'signal_type': signal_data['type'],
                'entry_price': levels['entry'],
                'stop_loss': levels['stop_loss'],
                'take_profit': levels['take_profit'],
                'funding_rate': metrics.get('funding_rate', 0),
                'open_interest': metrics.get('open_interest', 0),
                'indicators': indicators,
                'recommendations': self._generate_futures_recommendations(signal_data, metrics)
            }
            
        except Exception as e:
            print(f"Error in futures analysis: {e}")
            return self._get_default_analysis()

    def analyze_day_trading(self, market_data: Dict) -> Dict:
        """Análise para Day Trading"""
        try:
            volume_analysis = self._analyze_volume(market_data)
            price_analysis = self._analyze_price_action(market_data)
            signal_data = self._generate_day_trading_signal(volume_analysis, price_analysis)
            levels = self._calculate_day_trading_levels(market_data['price'], signal_data['signal'])
            
            return {
                'signal': signal_data['signal'],
                'signal_type': signal_data['type'],
                'buy_volume_percent': volume_analysis['buy_percent'],
                'sell_volume_percent': volume_analysis['sell_percent'],
                'trend_direction': price_analysis['trend'],
                'trend_strength': price_analysis['strength'],
                'volatility': price_analysis['volatility'],
                'entry_price': levels['entry'],
                'stop_loss': levels['stop_loss'],
                'take_profit': levels['take_profit'],
                'stop_loss_percent': levels['sl_percent'],
                'take_profit_percent': levels['tp_percent'],
                'recommendations': self._generate_day_trading_recommendations(signal_data, price_analysis)
            }
            
        except Exception as e:
            print(f"Error in day trading analysis: {e}")
            return self._get_default_analysis()

    def analyze_swing(self, market_data: Dict) -> Dict:
        """Análise para Swing Trading"""
        try:
            trend_analysis = self._analyze_trend(market_data)
            levels = self._analyze_key_levels(market_data)
            signal_data = self._generate_swing_signal(trend_analysis, levels)
            
            return {
                'signal': signal_data['signal'],
                'signal_type': signal_data['type'],
                'market_phase': trend_analysis['phase'],
                'primary_trend': trend_analysis['primary'],
                'secondary_trend': trend_analysis['secondary'],
                'key_levels': levels['key_levels'],
                'entry_price': signal_data['entry'],
                'stop_loss': signal_data['stop'],
                'take_profit_levels': signal_data['targets'],
                'tp_percentages': signal_data['target_percentages'],
                'expected_duration': '1-2 weeks',
                'recommendations': self._generate_swing_recommendations(signal_data)
            }
            
        except Exception as e:
            print(f"Error in swing analysis: {e}")
            return self._get_default_analysis()

    def analyze_position(self, market_data: Dict) -> Dict:
        """Análise para Position Trading"""
        try:
            cycle_analysis = self._analyze_market_cycle(market_data)
            fundamentals = self._analyze_fundamentals()
            signal_data = self._generate_position_signal(cycle_analysis, fundamentals)
            
            return {
                'signal': signal_data['signal'],
                'signal_type': signal_data['type'],
                'market_cycle_progress': cycle_analysis['progress'],
                'market_cycle_phase': cycle_analysis['phase'],
                'entry_price': signal_data['entry'],
                'stop_loss': signal_data['stop'],
                'take_profit': signal_data['target'],
                'accumulation_zones': self._calculate_accumulation_zones(market_data),
                'target_timeframe': '3-6 months',
                'recommendations': self._generate_position_recommendations(cycle_analysis)
            }
            
        except Exception as e:
            print(f"Error in position analysis: {e}")
            return self._get_default_analysis()

    def _calculate_technical_indicators(self, market_data: Dict) -> Dict:
        """Calcula indicadores técnicos básicos"""
        try:
            prices = market_data.get('historical_prices', [])
            if not prices:
                return self._get_default_indicators()
                
            # RSI
            rsi = self._calculate_rsi(prices)
            
            # MACD
            macd, signal = self._calculate_macd(prices)
            
            # Momentum
            momentum = self._calculate_momentum(prices)
            
            return {
                'rsi': rsi[-1] if len(rsi) > 0 else 50,
                'macd': macd[-1] if len(macd) > 0 else 0,
                'macd_signal': 'buy' if macd[-1] > signal[-1] else 'sell',
                'momentum': momentum[-1] if len(momentum) > 0 else 0,
                'momentum_signal': 'buy' if momentum[-1] > 0 else 'sell'
            }
        except Exception as e:
            print(f"Error calculating indicators: {e}")
            return self._get_default_indicators()

    def _calculate_rsi(self, prices: List[float], period: int = 14) -> List[float]:
        """Calcula o RSI (Relative Strength Index)"""
        try:
            if len(prices) < period + 1:
                return [50.0]  # Valor neutro

            deltas = np.diff(prices)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            avg_gain = np.mean(gains[:period])
            avg_loss = np.mean(losses[:period])
            
            if avg_loss == 0:
                return [100.0]
                
            rs = avg_gain / avg_loss
            rsi = [100 - (100 / (1 + rs))]
            
            for i in range(period, len(deltas)):
                avg_gain = ((avg_gain * (period - 1)) + gains[i]) / period
                avg_loss = ((avg_loss * (period - 1)) + losses[i]) / period
                if avg_loss == 0:
                    rsi.append(100.0)
                else:
                    rs = avg_gain / avg_loss
                    rsi.append(100 - (100 / (1 + rs)))
            
            return rsi
            
        except Exception as e:
            print(f"Error calculating RSI: {e}")
            return [50.0]

    def _calculate_macd(self, prices: List[float]) -> Tuple[List[float], List[float]]:
        """Calcula MACD (Moving Average Convergence Divergence)"""
        try:
            exp1 = self._calculate_ema(prices, 12)
            exp2 = self._calculate_ema(prices, 26)
            macd = [e1 - e2 for e1, e2 in zip(exp1, exp2)]
            signal = self._calculate_ema(macd, 9)
            return macd, signal
        except Exception as e:
            print(f"Error calculating MACD: {e}")
            return [0.0], [0.0]

    def _calculate_ema(self, data: List[float], span: int) -> List[float]:
        """Calcula EMA (Exponential Moving Average)"""
        try:
            alpha = 2.0 / (span + 1)
            ema = [data[0]]
            for price in data[1:]:
                ema.append(alpha * price + (1 - alpha) * ema[-1])
            return ema
        except Exception as e:
            print(f"Error calculating EMA: {e}")
            return [data[0]]

    def _analyze_volume(self, market_data: Dict) -> Dict:
        """Analisa perfil de volume"""
        try:
            current_volume = market_data.get('volume_24h', 0)
            avg_volume = market_data.get('avg_volume_24h', 0)
            
            if avg_volume == 0:
                return {'buy_percent': 50, 'sell_percent': 50}
                
            volume_ratio = current_volume / avg_volume
            
            if volume_ratio > 1.2:
                buy_percent = 60
                sell_percent = 40
            elif volume_ratio < 0.8:
                buy_percent = 40
                sell_percent = 60
            else:
                buy_percent = 50
                sell_percent = 50
                
            return {
                'buy_percent': buy_percent,
                'sell_percent': sell_percent,
                'ratio': volume_ratio
            }
        except Exception as e:
            print(f"Error analyzing volume: {e}")
            return {'buy_percent': 50, 'sell_percent': 50}

    def _analyze_price_action(self, market_data: Dict) -> Dict:
        """Analisa ação do preço"""
        try:
            prices = market_data.get('historical_prices', [])
            if not prices:
                return self._get_default_price_analysis()
                
            # Calcular tendência
            sma20 = np.mean(prices[-20:])
            sma50 = np.mean(prices[-50:])
            current_price = prices[-1]
            
            # Determinar direção
            if current_price > sma20 > sma50:
                trend = 'uptrend'
                strength = min((current_price - sma50) / sma50 * 100, 100)
            elif current_price < sma20 < sma50:
                trend = 'downtrend'
                strength = min((sma50 - current_price) / current_price * 100, 100)
            else:
                trend = 'neutral'
                strength = 50
                
            # Calcular volatilidade
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns) * np.sqrt(252) * 100
            
            return {
                'trend': trend,
                'strength': strength,
                'volatility': volatility
            }
        except Exception as e:
            print(f"Error analyzing price action: {e}")
            return self._get_default_price_analysis()

    def _analyze_market_cycle(self, market_data: Dict) -> Dict:
        """Analisa ciclo de mercado"""
        try:
            prices = market_data.get('historical_prices', [])
            ath = max(prices) if prices else market_data['price']
            atl = min(prices) if prices else market_data['price']
            current_price = market_data['price']
            
            # Calcular progresso no ciclo
            price_range = ath - atl
            if price_range == 0:
                return {'progress': 50, 'phase': 'undefined'}
                
            progress = ((current_price - atl) / price_range) * 100
            
            # Determinar fase
            if progress < 25:
                phase = 'accumulation'
            elif progress < 50:
                phase = 'markup'
            elif progress < 75:
                phase = 'distribution'
            else:
                phase = 'markdown'
                
            return {
                'progress': progress,
                'phase': phase,
                'ath': ath,
                'atl': atl
            }
        except Exception as e:
            print(f"Error analyzing market cycle: {e}")
            return {'progress': 50, 'phase': 'undefined'}

    def _analyze_fundamentals(self) -> Dict:
        """Analisa fatores fundamentais"""
        try:
            # Aqui você implementaria a análise de dados on-chain e outros fundamentais
            return {
                'network_health': 'strong',
                'adoption_metrics': 'increasing',
                'market_sentiment': 'positive'
            }
        except Exception as e:
            print(f"Error analyzing fundamentals: {e}")
            return {}

    def _generate_futures_signal(self, indicators: Dict) -> Dict:
        """Gera sinal para futures trading"""
        try:
            # Pesos para diferentes indicadores
            weights = {
                'rsi': 0.3,
                'macd': 0.4,
                'momentum': 0.3
            }
            
            # Calcular probabilidade de alta/baixa
            bull_score = 0
            bear_score = 0
            
            # RSI
            if indicators['rsi'] < 30:
                bull_score += weights['rsi']
            elif indicators['rsi'] > 70:
                bear_score += weights['rsi']
            
            # MACD
            if indicators['macd_signal'] == 'buy':
                bull_score += weights['macd']
            else:
                bear_score += weights['macd']
            
            # Momentum
            if indicators['momentum_signal'] == 'buy':
                bull_score += weights['momentum']
            else:
                bear_score += weights['momentum']
            
            # Determinar sinal final
            confidence = max(bull_score, bear_score) * 100
            
            if confidence < self.technical_threshold:
                return {'signal': 'neutral', 'type': 'neutral', 'confidence': confidence}
            
            return {
                'signal': 'buy' if bull_score > bear_score else 'sell',
                'type': 'buy' if bull_score > bear_score else 'sell',
                'confidence': confidence
            }
        except Exception as e:
            print(f"Error generating futures signal: {e}")
            return {'signal': 'neutral', 'type': 'neutral', 'confidence': 0}

    def _calculate_futures_levels(self, price: float, signal: str) -> Dict:
        """Calcula níveis para futures trading"""
        try:
            # Usar ATR ou volatilidade para ajustar níveis
            volatility = 0.02  # 2% como exemplo, ajustar baseado em ATR
            
            if signal == 'buy':
                entry = price * 0.998  # Entrada 0.2% abaixo
                stop = entry * (1 - volatility)  # Stop 2% abaixo
                target = entry * (1 + volatility * 2)  # Alvo 4% acima
            elif signal == 'sell':
                entry = price * 1.002  # Entrada 0.2% acima
                stop = entry * (1 + volatility)  # Stop 2% acima
                target = entry * (1 - volatility * 2)  # Alvo 4% abaixo
            else:
                return self._get_default_levels(price)
                
            return {
                'entry': entry,
                'stop_loss': stop,
                'take_profit': target
            }
        except Exception as e:
            print(f"Error calculating futures levels: {e}")
            return self._get_default_levels(price)

    def _calculate_futures_metrics(self, market_data: Dict) -> Dict:
        """Calcula métricas adicionais para futures"""
        try:
            return {
                'funding_rate': market_data.get('funding_rate', 0),
                'open_interest': market_data.get('open_interest', 0),
                'long_short_ratio': market_data.get('long_short_ratio', 1),
                'liquidations_24h': market_data.get('liquidations_24h', 0)
            }
        except Exception as e:
            print(f"Error calculating futures metrics: {e}")
            return {}

    def _generate_day_trading_signal(self, volume_analysis: Dict, price_analysis: Dict) -> Dict:
        """Gera sinal para day trading"""
        try:
            bull_score = 0
            bear_score = 0
            
            # Volume analysis
            if volume_analysis['buy_percent'] > 55:
                bull_score += 0.4
            elif volume_analysis['sell_percent'] > 55:
                bear_score += 0.4
            
            # Price action
            if price_analysis['trend'] == 'uptrend':
                bull_score += 0.6 * (price_analysis['strength'] / 100)
            elif price_analysis['trend'] == 'downtrend':
                bear_score += 0.6 * (price_analysis['strength'] / 100)
            
            confidence = max(bull_score, bear_score) * 100
            
            if confidence < self.technical_threshold:
                return {'signal': 'neutral', 'type': 'neutral', 'confidence': confidence}
            
            return {
                'signal': 'buy' if bull_score > bear_score else 'sell',
                'type': 'buy' if bull_score > bear_score else 'sell',
                'confidence': confidence
            }
        except Exception as e:
            print(f"Error generating day trading signal: {e}")
            return {'signal': 'neutral', 'type': 'neutral', 'confidence': 0}

    def _calculate_day_trading_levels(self, price: float, signal: str) -> Dict:
        """Calcula níveis para day trading"""
        try:
            volatility = 0.01  # 1% para day trading
            
            if signal == 'buy':
                entry = price * 0.999
                stop = entry * (1 - volatility)
                target = entry * (1 + volatility * 2)
            elif signal == 'sell':
                entry = price * 1.001
                stop = entry * (1 + volatility)
                target = entry * (1 - volatility * 2)
            else:
                return self._get_default_levels(price)
            
            sl_percent = abs((stop - entry) / entry * 100)
            tp_percent = abs((target - entry) / entry * 100)
            
            return {
                'entry': entry,
                'stop_loss': stop,
                'take_profit': target,
                'sl_percent': sl_percent,
                'tp_percent': tp_percent
            }
        except Exception as e:
            print(f"Error calculating day trading levels: {e}")
            return self._get_default_levels(price)

    def _generate_swing_signal(self, trend_analysis: Dict, levels: Dict) -> Dict:
        """Gera sinal para swing trading"""
        try:
            bull_score = 0
            bear_score = 0
            
            # Trend analysis
            if trend_analysis['primary'] == 'Bullish':
                bull_score += 0.4
            elif trend_analysis['primary'] == 'Bearish':
                bear_score += 0.4
                
            if trend_analysis['secondary'] == 'Bullish':
                bull_score += 0.3
            elif trend_analysis['secondary'] == 'Bearish':
                bear_score += 0.3
            
            # Market phase
            if trend_analysis['phase'] == 'Strong Uptrend':
                bull_score += 0.3
            elif trend_analysis['phase'] == 'Strong Downtrend':
                bear_score += 0.3
            
            confidence = max(bull_score, bear_score) * 100
            price = levels.get('current_price', 0)
            
            if confidence < self.technical_threshold:
                return self._get_default_signal(price)
            
            # Calcular targets
            targets = self._calculate_swing_targets(price, 'buy' if bull_score > bear_score else 'sell')
            
            return {
                'signal': 'buy' if bull_score > bear_score else 'sell',
                'type': 'buy' if bull_score > bear_score else 'sell',
                'confidence': confidence,
                'entry': price * 0.995 if bull_score > bear_score else price * 1.005,
                'stop': price * 0.97 if bull_score > bear_score else price * 1.03,
                'targets': targets,
                'target_percentages': [
                    abs((t - price) / price * 100) for t in targets
                ]
            }
        except Exception as e:
            print(f"Error generating swing signal: {e}")
            return self._get_default_signal(levels.get('current_price', 0))

    def _generate_position_signal(self, cycle_analysis: Dict, fundamentals: Dict) -> Dict:
        """Gera sinal para position trading"""
        try:
            bull_score = 0
            bear_score = 0
            
            # Cycle analysis
            progress = cycle_analysis['progress']
            if progress < 30:  # Fase inicial do ciclo
                bull_score += 0.4
            elif progress > 70:  # Fase final do ciclo
                bear_score += 0.4
            
            # Fundamental analysis
            if fundamentals.get('network_health') == 'strong':
                bull_score += 0.2
            if fundamentals.get('adoption_metrics') == 'increasing':
                bull_score += 0.2
            if fundamentals.get('market_sentiment') == 'positive':
                bull_score += 0.2
            
            confidence = max(bull_score, bear_score) * 100
            
            if confidence < self.technical_threshold:
                return self._get_default_signal(cycle_analysis.get('current_price', 0))
            
            current_price = cycle_analysis.get('current_price', 0)
            
            return {
                'signal': 'buy' if bull_score > bear_score else 'sell',
                'type': 'buy' if bull_score > bear_score else 'sell',
                'confidence': confidence,
                'entry': current_price * 0.98 if bull_score > bear_score else current_price * 1.02,
                'stop': current_price * 0.85 if bull_score > bear_score else current_price * 1.15,
                'target': current_price * 1.5 if bull_score > bear_score else current_price * 0.5
            }
        except Exception as e:
            print(f"Error generating position signal: {e}")
            return self._get_default_signal(cycle_analysis.get('current_price', 0))

    def _get_default_indicators(self) -> Dict:
        """Retorna indicadores padrão"""
        return {
            'rsi': 50,
            'macd': 0,
            'macd_signal': 'neutral',
            'momentum': 0,
            'momentum_signal': 'neutral'
        }

    def _get_default_analysis(self) -> Dict:
        """Retorna análise padrão"""
        return {
            'signal': 'neutral',
            'signal_type': 'neutral',
            'entry_price': 0,
            'stop_loss': 0,
            'take_profit': 0,
            'confidence': 0,
            'recommendations': []
        }

    def _get_default_levels(self, price: float) -> Dict:
        """Retorna níveis padrão"""
        return {
            'entry': price,
            'stop_loss': price * 0.98,
            'take_profit': price * 1.02
        }

    def _get_default_signal(self, price: float) -> Dict:
        """Retorna sinal padrão"""
        return {
            'signal': 'neutral',
            'type': 'neutral',
            'confidence': 0,
            'entry': price,
            'stop': price * 0.98,
            'target': price * 1.02
        }

    def _get_default_price_analysis(self) -> Dict:
        """Retorna análise de preço padrão"""
        return {
            'trend': 'neutral',
            'strength': 50,
            'volatility': 0
        }

    def _generate_futures_recommendations(self, signal_data: Dict, metrics: Dict) -> List[Dict]:
        """Gera recomendações para futures trading"""
        recommendations = []
        
        # Recomendação baseada no funding rate
        if metrics.get('funding_rate', 0) > 0.01:
            recommendations.append({
                'type': 'warning',
                'icon': 'exclamation-triangle',
                'text': 'Alto funding rate, considere aguardar normalização'
            })
            
        # Recomendação baseada na proporção long/short
        long_short_ratio = metrics.get('long_short_ratio', 1)
        if long_short_ratio > 2:
            recommendations.append({
                'type': 'warning',
                'icon': 'chart-line',
                'text': 'Mercado muito alavancado em long, risco de liquidação em cascata'
            })
        elif long_short_ratio < 0.5:
            recommendations.append({
                'type': 'warning',
                'icon': 'chart-line',
                'text': 'Mercado muito alavancado em short, risco de short squeeze'
            })
            
        # Recomendação baseada na confiança do sinal
        if signal_data['confidence'] > 80:
            recommendations.append({
                'type': 'success',
                'icon': 'check-circle',
                'text': 'Sinal forte, considere entrada agressiva'
            })
        elif signal_data['confidence'] < 70:
            recommendations.append({
                'type': 'info',
                'icon': 'info-circle',
                'text': 'Sinal moderado, considere entrada parcial'
            })
            
        return recommendations

    def _calculate_swing_targets(self, price: float, direction: str) -> List[float]:
        """Calcula alvos para swing trading"""
        if direction == 'buy':
            return [
                price * 1.05,  # Target 1: +5%
                price * 1.10,  # Target 2: +10%
                price * 1.15   # Target 3: +15%
            ]
        else:
            return [
                price * 0.95,  # Target 1: -5%
                price * 0.90,  # Target 2: -10%
                price * 0.85   # Target 3: -15%
            ]