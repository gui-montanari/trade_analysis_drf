from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services.market_data import MarketDataService
from .services.analysis_service import AnalysisService
from .services.risk_manager import RiskManager
from datetime import datetime
from .services.notification_service import NotificationService


market_service = MarketDataService()
analysis_service = AnalysisService()
risk_manager = RiskManager()

@login_required
def futures_analysis(request):
    """View para análise de Futures Trading"""
    try:
        # Obter dados do mercado
        market_data = market_service.get_current_data()
        
        # Gerar análise
        analysis = analysis_service.analyze_futures(market_data)
        
        # Calcular métricas de risco
        risk_metrics = risk_manager.calculate_futures_risk(analysis)

                # Criar notificações, se necessário
        NotificationService.create_signal_notification(request.user, analysis, 'futures')
        NotificationService.create_risk_notification(request.user, risk_metrics, 'futures')
        
        # Obter notificações não lidas para o contexto
        unread_notifications = NotificationService.get_user_notifications(
            request.user, unread_only=True
        )
        unread_count = NotificationService.get_unread_count(request.user)
        
        
        # Formatar dados para o template
        context = {
            'market_data': {
                'price': market_data.get('price', 0),
                'change_24h': market_data.get('change_24h', 0),
                'volume_24h': market_data.get('volume_24h', 0) / 1e9,  # Converter para bilhões
                'funding_rate': market_data.get('funding_rate', 0),
                'open_interest': market_data.get('open_interest', 0) / 1e9
            },
            'analysis': analysis,
            'risk_metrics': risk_metrics,
            'indicators': analysis.get('indicators', []),
            'signal': {
                'type': analysis.get('signal_type', 'neutral'),
                'signal': analysis.get('signal', 'NEUTRAL'),
                'entry_price': analysis.get('entry_price', 0),
                'stop_loss': analysis.get('stop_loss', 0),
                'take_profit': analysis.get('take_profit', 0)
            },
            'last_update': datetime.now().strftime('%H:%M:%S'),
            'unread_notifications': unread_notifications,
            'unread_count': unread_count
        }
        
        return render(request, 'analysis/futures.html', context)
        
    except Exception as e:
        print(f"Error in futures analysis view: {e}")
        return render(request, 'analysis/futures.html', {'error': str(e)})

@login_required
def day_trading_analysis(request):
    """View para análise de Day Trading"""
    try:
        market_data = market_service.get_current_data()
        analysis = analysis_service.analyze_day_trading(market_data)
        risk_metrics = risk_manager.calculate_day_trading_risk(analysis)
        
        context = {
            'market_data': market_data,
            'analysis': {
                'buy_volume_percent': analysis.get('buy_volume_percent', 50),
                'sell_volume_percent': analysis.get('sell_volume_percent', 50),
                'vwap': analysis.get('vwap', 0),
                'price_to_vwap': analysis.get('price_to_vwap', 0),
                'resistance_level': analysis.get('resistance_level', 0),
                'support_level': analysis.get('support_level', 0),
                'intraday_indicators': analysis.get('intraday_indicators', []),
                'signal_type': analysis.get('signal_type', 'neutral'),
                'signal': analysis.get('signal', 'NEUTRAL'),
                'intraday_trend': analysis.get('intraday_trend', {'direction': 'Undefined', 'color': 'secondary'}),
                'trend_strength': analysis.get('trend_strength', 0),
                'volatility': analysis.get('volatility', 0),
                'entry_price': analysis.get('entry_price', 0),
                'stop_loss': analysis.get('stop_loss', 0),
                'take_profit': analysis.get('take_profit', 0),
                'stop_loss_percent': analysis.get('stop_loss_percent', 0),
                'take_profit_percent': analysis.get('take_profit_percent', 0),
                'attention_points': analysis.get('attention_points', []),
                'day_trading_tips': analysis.get('day_trading_tips', [])
            },
            'risk_metrics': risk_metrics,
            'last_update': datetime.now().strftime('%H:%M:%S')
        }
        
        return render(request, 'analysis/daytrading.html', context)
        
    except Exception as e:
        print(f"Error in day trading analysis view: {e}")
        return render(request, 'analysis/daytrading.html', {'error': str(e)})

@login_required
def swing_analysis(request):
    """View para análise de Swing Trading"""
    try:
        market_data = market_service.get_current_data()
        analysis = analysis_service.analyze_swing(market_data)
        risk_metrics = risk_manager.calculate_swing_risk(analysis)
        
        context = {
            'market_data': market_data,
            'analysis': {
                'market_phase': analysis.get('market_phase', 'Undefined'),
                'primary_trend': analysis.get('primary_trend', {'direction': 'Undefined', 'color': 'secondary'}),
                'secondary_trend': analysis.get('secondary_trend', {'direction': 'Undefined', 'color': 'secondary'}),
                'key_levels': analysis.get('key_levels', []),
                'technical_indicators': analysis.get('technical_indicators', []),
                'signal_type': analysis.get('signal_type', 'neutral'),
                'signal': analysis.get('signal', 'NEUTRAL'),
                'trend_strength': analysis.get('trend_strength', 0),
                'momentum_score': analysis.get('momentum_score', 0),
                'momentum_description': analysis.get('momentum_description', ''),
                'expected_duration': analysis.get('expected_duration', '1-2 weeks'),
                'entry_price': analysis.get('entry_price', 0),
                'stop_loss': analysis.get('stop_loss', 0),
                'take_profit_levels': analysis.get('take_profit_levels', []),
                'tp_percentages': analysis.get('tp_percentages', []),
                'position_size': analysis.get('position_size', 0),
                'attention_points': analysis.get('attention_points', []),
                'entry_points': analysis.get('entry_points', []),
                'exit_points': analysis.get('exit_points', [])
            },
            'risk_metrics': risk_metrics,
            'last_update': datetime.now().strftime('%H:%M:%S')
        }
        
        return render(request, 'analysis/swing.html', context)
        
    except Exception as e:
        print(f"Error in swing analysis view: {e}")
        return render(request, 'analysis/swing.html', {'error': str(e)})

@login_required
def position_analysis(request):
    """View para análise de Position Trading"""
    try:
        market_data = market_service.get_current_data()
        analysis = analysis_service.analyze_position(market_data)
        risk_metrics = risk_manager.calculate_position_risk(analysis)
        
        context = {
            'market_data': {
                'price': market_data.get('price', 0),
                'change_24h': market_data.get('change_24h', 0),
                'dominance': market_data.get('btc_dominance', 0),
                'dominance_change': market_data.get('dominance_change', 0)
            },
            'cycle_progress': analysis.get('market_cycle_progress', 50),
            'cycle_phase': analysis.get('market_cycle_phase', 'Undefined'),
            'analysis': {
                'onchain_metrics': analysis.get('onchain_metrics', []),
                'longterm_indicators': analysis.get('longterm_indicators', []),
                'macro_factors': analysis.get('macro_factors', []),
                'bullish_factors': analysis.get('bullish_factors', []),
                'bearish_factors': analysis.get('bearish_factors', []),
                'signal_type': analysis.get('signal_type', 'neutral'),
                'signal': analysis.get('signal', 'NEUTRAL'),
                'entry_price': analysis.get('entry_price', 0),
                'accumulation_zones': analysis.get('accumulation_zones', 0),
                'price_targets': analysis.get('price_targets', []),
                'allocation_percentage': analysis.get('allocation_percentage', 0),
                'dca_strategy': analysis.get('dca_strategy', [])
            },
            'risk_metrics': risk_metrics,
            'last_update': datetime.now().strftime('%H:%M:%S')
        }
        
        return render(request, 'analysis/position.html', context)
        
    except Exception as e:
        print(f"Error in position analysis view: {e}")
        return render(request, 'analysis/position.html', {'error': str(e)})

# Endpoints AJAX para atualização em tempo real
@login_required
def refresh_futures(request):
    """Endpoint AJAX para atualizar análise futures"""
    try:
        market_data = market_service.get_current_data()
        analysis = analysis_service.analyze_futures(market_data)
        risk_metrics = risk_manager.calculate_futures_risk(analysis)
        
        return JsonResponse({
            'success': True,
            'data': {
                'market_data': market_data,
                'analysis': analysis,
                'risk_metrics': risk_metrics,
                'last_update': datetime.now().strftime('%H:%M:%S')
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def refresh_daytrading(request):
    """Endpoint AJAX para atualizar análise day trading"""
    try:
        market_data = market_service.get_current_data()
        analysis = analysis_service.analyze_day_trading(market_data)
        risk_metrics = risk_manager.calculate_day_trading_risk(analysis)
        
        return JsonResponse({
            'success': True,
            'data': {
                'market_data': market_data,
                'analysis': analysis,
                'risk_metrics': risk_metrics,
                'last_update': datetime.now().strftime('%H:%M:%S')
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def refresh_swing(request):
    """Endpoint AJAX para atualizar análise swing"""
    try:
        market_data = market_service.get_current_data()
        analysis = analysis_service.analyze_swing(market_data)
        risk_metrics = risk_manager.calculate_swing_risk(analysis)
        
        return JsonResponse({
            'success': True,
            'data': {
                'market_data': market_data,
                'analysis': analysis,
                'risk_metrics': risk_metrics,
                'last_update': datetime.now().strftime('%H:%M:%S')
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def refresh_position(request):
    """Endpoint AJAX para atualizar análise position"""
    try:
        market_data = market_service.get_current_data()
        analysis = analysis_service.analyze_position(market_data)
        risk_metrics = risk_manager.calculate_position_risk(analysis)
        
        return JsonResponse({
            'success': True,
            'data': {
                'market_data': market_data,
                'analysis': analysis,
                'risk_metrics': risk_metrics,
                'last_update': datetime.now().strftime('%H:%M:%S')
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })