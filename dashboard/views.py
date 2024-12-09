from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from analysis.services.market_data import MarketDataService
from analysis.services.analysis_service import AnalysisService

market_service = MarketDataService()
analysis_service = AnalysisService()

@login_required
def dashboard(request):
    """View principal do dashboard"""
    try:
        # Obter dados do mercado
        market_data = market_service.get_current_data()
        
        # Obter análises recentes
        recent_analyses = {
            'futures': analysis_service.analyze_futures(market_data),
            'day': analysis_service.analyze_day_trading(market_data),
            'swing': analysis_service.analyze_swing(market_data),
            'position': analysis_service.analyze_position(market_data)
        }
        
        context = {
            'market_data': {
                'price': market_data.get('price', 0),
                'change_24h': market_data.get('change_24h', 0),
                'volume_24h': market_data.get('volume_24h', 0),
                'volume_change': market_data.get('volume_change_24h', 0),
                'market_cap': market_data.get('market_cap', 0),
                'dominance': market_data.get('btc_dominance', 0),
                'sentiment': _get_market_sentiment(market_data)
            },
            'recent_analyses': recent_analyses,
            'technical_indicators': _get_technical_indicators(market_data)
        }
        
        return render(request, 'dashboard/dashboard.html', context)
        
    except Exception as e:
        print(f"Error in dashboard view: {e}")
        return render(request, 'dashboard/dashboard.html', {'error': str(e)})

@login_required
def refresh_data(request):
    """Endpoint AJAX para atualizar dados do dashboard"""
    try:
        market_data = market_service.get_current_data()
        analysis = analysis_service.analyze_futures(market_data)
        
        return JsonResponse({
            'success': True,
            'data': {
                'price': market_data.get('price', 0),
                'change_24h': market_data.get('change_24h', 0),
                'volume_24h': market_data.get('volume_24h', 0),
                'dominance': market_data.get('btc_dominance', 0),
                'analysis': analysis
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

def _get_market_sentiment(market_data: dict) -> dict:
    """Calcula o sentimento do mercado"""
    try:
        # Lógica simples de sentimento baseada em indicadores
        bullish_factors = 0
        total_factors = 3
        
        if market_data.get('change_24h', 0) > 0:
            bullish_factors += 1
        if market_data.get('volume_change_24h', 0) > 0:
            bullish_factors += 1
        if market_data.get('dominance_change', 0) > 0:
            bullish_factors += 1
            
        sentiment_score = (bullish_factors / total_factors) * 100
        
        if sentiment_score >= 66:
            return {'status': 'Bullish', 'strength': 'Strong'}
        elif sentiment_score >= 33:
            return {'status': 'Neutral', 'strength': 'Moderate'}
        else:
            return {'status': 'Bearish', 'strength': 'Strong'}
            
    except Exception as e:
        print(f"Error calculating market sentiment: {e}")
        return {'status': 'Neutral', 'strength': 'Unknown'}

def _get_technical_indicators(market_data: dict) -> list:
    """Obtém indicadores técnicos principais"""
    try:
        indicators = analysis_service._calculate_technical_indicators(market_data)
        
        return [
            {
                'name': 'RSI (14)',
                'value': indicators['rsi'],
                'signal': 'COMPRA' if indicators['rsi'] < 30 else 'VENDA' if indicators['rsi'] > 70 else 'NEUTRO'
            },
            {
                'name': 'MACD',
                'value': indicators['macd'],
                'signal': indicators['macd_signal']
            },
            {
                'name': 'Momentum',
                'value': indicators['momentum'],
                'signal': indicators['momentum_signal']
            }
        ]
        
    except Exception as e:
        print(f"Error getting technical indicators: {e}")
        return []