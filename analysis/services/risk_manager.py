from typing import Dict, List, Optional, Union
import numpy as np
from datetime import datetime

class RiskManager:
    def __init__(self):
        self.max_position_size = 0.1  # 10% máximo do capital
        self.min_risk_reward = 2.0    # Mínimo risco/retorno
        self.max_futures_leverage = 10 # Alavancagem máxima
        
    def calculate_futures_risk(self, analysis: Dict) -> Dict:
        """Calcula métricas de risco para futures trading"""
        try:
            entry_price = analysis['entry_price']
            stop_loss = analysis['stop_loss']
            take_profit = analysis['take_profit']
            
            # Calcular risco/retorno
            risk = abs(entry_price - stop_loss)
            reward = abs(take_profit - entry_price)
            risk_reward = reward / risk if risk > 0 else 0
            
            # Calcular retorno potencial com alavancagem
            potential_return = (reward / entry_price) * 100 * self.max_futures_leverage
            max_risk = (risk / entry_price) * 100 * self.max_futures_leverage
            
            # Ajustar tamanho da posição baseado no risco
            position_size = self._calculate_position_size(max_risk)
            
            # Determinar alavancagem recomendada
            recommended_leverage = self._calculate_recommended_leverage(potential_return, max_risk)
            
            return {
                'risk_reward_ratio': risk_reward,
                'potential_return': potential_return,
                'max_risk': max_risk,
                'position_size': position_size,
                'recommended_leverage': recommended_leverage,
                'recommendations': self._generate_risk_recommendations(risk_reward, max_risk)
            }
            
        except Exception as e:
            print(f"Error calculating futures risk: {e}")
            return self._get_default_risk_metrics()

    def calculate_day_trading_risk(self, analysis: Dict) -> Dict:
        """Calcula métricas de risco para day trading"""
        try:
            entry_price = analysis['entry_price']
            stop_loss = analysis['stop_loss']
            take_profit = analysis['take_profit']
            
            # Calcular métricas básicas
            risk = abs(entry_price - stop_loss)
            reward = abs(take_profit - entry_price)
            risk_reward = reward / risk if risk > 0 else 0
            
            # Calcular retornos percentuais
            risk_percent = (risk / entry_price) * 100
            reward_percent = (reward / entry_price) * 100
            
            # Ajustar tamanho da posição
            position_size = self._calculate_position_size(risk_percent)
            
            return {
                'risk_reward_ratio': risk_reward,
                'risk_percent': risk_percent,
                'reward_percent': reward_percent,
                'recommended_position_size': position_size,
                'max_loss_amount': risk * position_size,
                'recommendations': self._generate_day_trading_recommendations(risk_reward, risk_percent)
            }
            
        except Exception as e:
            print(f"Error calculating day trading risk: {e}")
            return self._get_default_risk_metrics()

    def calculate_swing_risk(self, analysis: Dict) -> Dict:
        """Calcula métricas de risco para swing trading"""
        try:
            entry_price = analysis['entry_price']
            stop_loss = analysis['stop_loss']
            targets = analysis['take_profit_levels']
            
            # Calcular risco médio e recompensa média
            risk = abs(entry_price - stop_loss)
            avg_reward = np.mean([abs(t - entry_price) for t in targets])
            risk_reward = avg_reward / risk if risk > 0 else 0
            
            # Calcular trailing stop
            atr = self._calculate_atr(analysis.get('historical_prices', []))
            trailing_stop = max(2 * atr, risk)
            
            # Ajustar posição baseado na volatilidade
            position_size = self._calculate_swing_position_size(risk, atr)
            
            return {
                'risk_reward_ratio': risk_reward,
                'recommended_position_size': position_size,
                'trailing_stop': trailing_stop,
                'risk_per_trade': (risk / entry_price) * 100,
                'max_drawdown': self._calculate_max_drawdown(position_size, risk),
                'recommendations': self._generate_swing_recommendations(risk_reward, position_size)
            }
            
        except Exception as e:
            print(f"Error calculating swing risk: {e}")
            return self._get_default_risk_metrics()

    def calculate_position_risk(self, analysis: Dict) -> Dict:
        """Calcula métricas de risco para position trading"""
        try:
            cycle_progress = analysis['market_cycle_progress']
            current_price = analysis['entry_price']
            
            # Calcular alocação recomendada baseada no ciclo
            recommended_allocation = self._calculate_cycle_based_allocation(cycle_progress)
            
            # Calcular alvos de preço
            price_targets = self._calculate_position_targets(current_price, cycle_progress)
            
            # Gerar estratégia DCA
            dca_strategy = self._generate_dca_strategy(cycle_progress, recommended_allocation)
            
            return {
                'recommended_allocation': recommended_allocation,
                'price_targets': price_targets,
                'dca_strategy': dca_strategy,
                'max_portfolio_risk': recommended_allocation * 0.5,  # 50% do valor alocado
                'rebalancing_threshold': 20,  # Rebalancear a cada 20% de movimento
                'recommendations': self._generate_position_recommendations(cycle_progress)
            }
            
        except Exception as e:
            print(f"Error calculating position risk: {e}")
            return self._get_default_risk_metrics()

    def _calculate_position_size(self, risk_percent: float) -> float:
        """Calcula tamanho da posição baseado no risco"""
        max_risk = 0.02  # 2% máximo de risco por trade
        return min(self.max_position_size, (max_risk / risk_percent) * 100)

    def _calculate_recommended_leverage(self, potential_return: float, max_risk: float) -> int:
        """Calcula alavancagem recomendada"""
        if max_risk > 10:  # Se risco é muito alto
            return 1
        elif max_risk > 5:
            return min(5, self.max_futures_leverage)
        else:
            return min(10, self.max_futures_leverage)

    def _generate_risk_recommendations(self, risk_reward: float, max_risk: float) -> List[Dict]:
        """Gera recomendações de gestão de risco"""
        recommendations = []
        
        if risk_reward < self.min_risk_reward:
            recommendations.append({
                'type': 'warning',
                'icon': 'fa-exclamation-triangle',
                'text': 'Risco/Retorno abaixo do recomendado'
            })
            
        if max_risk > 5:
            recommendations.append({
                'type': 'danger',
                'icon': 'fa-radiation',
                'text': 'Alto risco detectado, reduza posição'
            })
            
        return
    
    def _calculate_atr(self, prices: List[float], period: int = 14) -> float:
            """Calcula o Average True Range"""
            try:
                if len(prices) < period:
                    return 0.0
                    
                highs = [max(prices[i:i+2]) for i in range(len(prices)-1)]
                lows = [min(prices[i:i+2]) for i in range(len(prices)-1)]
                
                true_ranges = []
                for i in range(len(highs)):
                    true_ranges.append(highs[i] - lows[i])
                    
                return np.mean(true_ranges[-period:])
                
            except Exception as e:
                print(f"Error calculating ATR: {e}")
                return 0.0
            
    def _calculate_swing_position_size(self, risk: float, atr: float) -> float:
        """Calcula tamanho da posição para swing trading baseado no ATR"""
        try:
            # Ajusta posição baseado na volatilidade
            volatility_factor = min(1.0, 0.02 / (atr / risk))
            base_position = self.max_position_size * volatility_factor
            
            return min(base_position, self.max_position_size)
            
        except Exception as e:
            print(f"Error calculating swing position size: {e}")
            return self.max_position_size * 0.5

    def _calculate_max_drawdown(self, position_size: float, risk: float) -> float:
        """Calcula drawdown máximo esperado"""
        return position_size * risk

    def _calculate_cycle_based_allocation(self, cycle_progress: float) -> float:
        """Calcula alocação baseada no ciclo de mercado"""
        try:
            # Ciclo dividido em quartis
            if cycle_progress <= 25:  # Acumulação
                return self.max_position_size * 0.8
            elif cycle_progress <= 50:  # Markup
                return self.max_position_size
            elif cycle_progress <= 75:  # Distribuição
                return self.max_position_size * 0.5
            else:  # Markdown
                return self.max_position_size * 0.3
                
        except Exception as e:
            print(f"Error calculating cycle allocation: {e}")
            return self.max_position_size * 0.5

    def _calculate_position_targets(self, current_price: float, cycle_progress: float) -> List[Dict]:
        """Calcula alvos de preço para position trading"""
        try:
            targets = []
            
            if cycle_progress <= 50:  # Fase de alta
                targets = [
                    {
                        'name': 'Target 1',
                        'price': current_price * 1.5,
                        'timeframe': '3-6 months'
                    },
                    {
                        'name': 'Target 2',
                        'price': current_price * 2.0,
                        'timeframe': '6-12 months'
                    },
                    {
                        'name': 'Target 3',
                        'price': current_price * 3.0,
                        'timeframe': '12-18 months'
                    }
                ]
            else:  # Fase de baixa
                targets = [
                    {
                        'name': 'Support 1',
                        'price': current_price * 0.8,
                        'timeframe': '1-3 months'
                    },
                    {
                        'name': 'Support 2',
                        'price': current_price * 0.6,
                        'timeframe': '3-6 months'
                    },
                    {
                        'name': 'Support 3',
                        'price': current_price * 0.4,
                        'timeframe': '6-12 months'
                    }
                ]
                
            return targets
            
        except Exception as e:
            print(f"Error calculating position targets: {e}")
            return []

    def _generate_dca_strategy(self, cycle_progress: float, allocation: float) -> List[Dict]:
        """Gera estratégia de Dollar Cost Average"""
        try:
            total_investment = allocation
            intervals = []
            
            if cycle_progress <= 25:  # Acumulação
                intervals = [
                    {
                        'percentage': 40,
                        'timing': 'Imediato',
                        'reason': 'Fase de acumulação inicial'
                    },
                    {
                        'percentage': 30,
                        'timing': 'Em 30 dias',
                        'reason': 'Aguardar possível queda'
                    },
                    {
                        'percentage': 30,
                        'timing': 'Em 60 dias',
                        'reason': 'Completar posição'
                    }
                ]
            elif cycle_progress <= 50:  # Markup
                intervals = [
                    {
                        'percentage': 50,
                        'timing': 'Imediato',
                        'reason': 'Aproveitar tendência de alta'
                    },
                    {
                        'percentage': 50,
                        'timing': 'Em correções',
                        'reason': 'Aguardar pullbacks'
                    }
                ]
            else:  # Distribuição/Markdown
                intervals = [
                    {
                        'percentage': 20,
                        'timing': 'Imediato',
                        'reason': 'Posição inicial reduzida'
                    },
                    {
                        'percentage': 40,
                        'timing': 'Após queda de 20%',
                        'reason': 'Aumentar em suportes'
                    },
                    {
                        'percentage': 40,
                        'timing': 'Após queda de 40%',
                        'reason': 'Completar posição em forte queda'
                    }
                ]
                
            return intervals
            
        except Exception as e:
            print(f"Error generating DCA strategy: {e}")
            return []

    def _get_default_risk_metrics(self) -> Dict:
        """Retorna métricas de risco padrão"""
        return {
            'risk_reward_ratio': 0.0,
            'potential_return': 0.0,
            'max_risk': 0.0,
            'position_size': 0.0,
            'recommended_leverage': 1,
            'recommendations': []
        }