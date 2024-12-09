from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch

class AnalysisViewsTest(TestCase):
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar um usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Criar um cliente de teste
        self.client = Client()
        
        # Dados mockados para testes
        self.mock_market_data = {
            'price': 42000.0,
            'change_24h': 2.5,
            'volume_24h': 25000000000,
            'btc_dominance': 48.2,
            'funding_rate': 0.01,
            'open_interest': 15000000000
        }
        
        self.mock_analysis = {
            'signal_type': 'buy',
            'signal': 'COMPRA',
            'entry_price': 41800.0,
            'stop_loss': 41000.0,
            'take_profit': 44000.0,
            'indicators': []
        }
        
        self.mock_risk_metrics = {
            'risk_reward_ratio': 2.5,
            'position_size': 10.0,
            'max_risk': 2.0
        }

    def test_login_required(self):
        """Testar se as views requerem login"""
        # Tentar acessar as páginas sem login
        urls = [
            reverse('analysis:futures'),
            reverse('analysis:daytrading'),
            reverse('analysis:swing'),
            reverse('analysis:position')
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)  # Deve redirecionar para login
            self.assertTrue(response.url.startswith('/users/login/'))

    @patch('analysis.views.market_service.get_current_data')
    @patch('analysis.views.analysis_service.analyze_futures')
    @patch('analysis.views.risk_manager.calculate_futures_risk')
    def test_futures_analysis_view(self, mock_risk, mock_analysis, mock_market):
        """Testar a view de análise futures"""
        # Configurar os mocks
        mock_market.return_value = self.mock_market_data
        mock_analysis.return_value = self.mock_analysis
        mock_risk.return_value = self.mock_risk_metrics
        
        # Fazer login
        self.client.login(username='testuser', password='testpass123')
        
        # Acessar a página
        response = self.client.get(reverse('analysis:futures'))
        
        # Verificar resposta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analysis/futures.html')
        
        # Verificar contexto
        self.assertIn('market_data', response.context)
        self.assertIn('analysis', response.context)
        self.assertIn('risk_metrics', response.context)

    @patch('analysis.views.market_service.get_current_data')
    @patch('analysis.views.analysis_service.analyze_day_trading')
    def test_daytrading_analysis_view(self, mock_analysis, mock_market):
        """Testar a view de análise day trading"""
        # Configurar os mocks
        mock_market.return_value = self.mock_market_data
        mock_analysis.return_value = {
            'buy_volume_percent': 60,
            'sell_volume_percent': 40,
            'signal_type': 'buy',
            'signal': 'COMPRA'
        }
        
        # Fazer login
        self.client.login(username='testuser', password='testpass123')
        
        # Acessar a página
        response = self.client.get(reverse('analysis:daytrading'))
        
        # Verificar resposta
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analysis/daytrading.html')

    def test_refresh_endpoints(self):
        """Testar endpoints de atualização AJAX"""
        # Fazer login
        self.client.login(username='testuser', password='testpass123')
        
        # Testar cada endpoint
        endpoints = [
            'refresh_futures',
            'refresh_daytrading',
            'refresh_swing',
            'refresh_position'
        ]
        
        for endpoint in endpoints:
            with patch('analysis.views.market_service.get_current_data') as mock_market:
                mock_market.return_value = self.mock_market_data
                
                response = self.client.get(reverse(f'analysis:{endpoint}'))
                
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.json()['success'])

    def test_error_handling(self):
        """Testar tratamento de erros"""
        # Fazer login
        self.client.login(username='testuser', password='testpass123')
        
        # Simular erro no serviço
        with patch('analysis.views.market_service.get_current_data') as mock_market:
            mock_market.side_effect = Exception('API Error')
            
            response = self.client.get(reverse('analysis:futures'))
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('error', response.context)

class AnalysisIntegrationTest(TestCase):
    """Testes de integração para as análises"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_complete_analysis_flow(self):
        """Testar fluxo completo de análise"""
        # Acessar cada tipo de análise em sequência
        analyses = ['futures', 'daytrading', 'swing', 'position']
        
        for analysis_type in analyses:
            # Acessar página de análise
            response = self.client.get(reverse(f'analysis:{analysis_type}'))
            self.assertEqual(response.status_code, 200)
            
            # Atualizar dados via AJAX
            refresh_response = self.client.get(
                reverse(f'analysis:refresh_{analysis_type}')
            )
            self.assertEqual(refresh_response.status_code, 200)
            
            # Verificar formato da resposta AJAX
            data = refresh_response.json()
            self.assertTrue(data['success'])
            self.assertIn('data', data)
            self.assertIn('market_data', data['data'])