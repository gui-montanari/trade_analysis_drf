from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from analysis.services.market_data import MarketDataService
from analysis.services.analysis_service import AnalysisService

market_service = MarketDataService()
analysis_service = AnalysisService()

@login_required
def dashboard_home(request):
    """View principal do dashboard"""
    try:
        # Obter dados do mercado
        market_data = market_service.get_current_data()
        
        context = {
            'market_data': {
                'price': market_data.get('price', 0),
                'change_24h': market_data.get('change_24h', 0),
                'volume_24h': market_data.get('volume_24h', 0),
                'volume_change': market_data.get('volume_change_24h', 0),
                'market_cap': market_data.get('market_cap', 0),
                'dominance': market_data.get('btc_dominance', 0),
            }
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
        
        return JsonResponse({
            'success': True,
            'data': {
                'price': market_data.get('price', 0),
                'change_24h': market_data.get('change_24h', 0),
                'volume_24h': market_data.get('volume_24h', 0),
                'dominance': market_data.get('btc_dominance', 0),
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })