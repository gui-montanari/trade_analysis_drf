from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services.market_data import MarketDataService
from .services.analysis_service import AnalysisService
from .services.risk_manager import RiskManager

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
        
        context = {
            'market_data': {
                'price': market_data.get('price', 0),
                'change_24h': market_data.get('change_24h', 0),
                'volume_24h': market_data.get('volume_24h') / 1e9,  # Converter para bilhões
                'funding_rate': market_data.get('funding_rate', 0),
                'open_interest': market_data.get('open_interest', 0) / 1e9  # Converter para bilhões
            },
            'indicators': analysis.get('indicators', []),
            'signal': analysis.get('signal_data', {}),
            'risk_metrics': risk_metrics,
            'recommendations': analysis.get('recommendations', [])
        }
        
        return render(request, 'analysis/futures.html', context)
        
    except Exception as e:
        print(f"Error in futures analysis view: {e}")
        return render(request, 'analysis/futures.html', {'error': str(e)})

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
                'market_data': {
                    'price': market_data.get('price', 0),
                    'change_24h': market_data.get('change_24h', 0),
                    'volume_24h': market_data.get('volume_24h') / 1e9,
                    'funding_rate': market_data.get('funding_rate', 0),
                    'open_interest': market_data.get('open_interest', 0) / 1e9
                },
                'analysis': analysis,
                'risk_metrics': risk_metrics
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })