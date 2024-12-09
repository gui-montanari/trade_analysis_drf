// Função para atualizar a análise
function refreshAnalysis(analysisType) {
    fetch(`/analysis/refresh/${analysisType}/`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateAnalysisUI(data.data, analysisType);
            } else {
                console.error('Error refreshing analysis:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
}

// Função para atualizar a UI
function updateAnalysisUI(data, analysisType) {
    // Atualizar preço
    document.querySelector('.price-large').innerHTML = `$${data.price.toFixed(2)}`;
    
    // Atualizar indicadores técnicos
    const indicators = document.querySelectorAll('.indicator-card');
    data.technical_indicators.forEach((indicator, index) => {
        if (indicators[index]) {
            indicators[index].querySelector('.analysis-badge').textContent = indicator.value;
            indicators[index].className = `indicator-card ${indicator.signal}`;
        }
    });
    
    // Atualizar sinal de trading
    const signalBadge = document.querySelector('.analysis-badge');
    if (signalBadge) {
        signalBadge.textContent = data.signal;
        signalBadge.className = `analysis-badge badge-${data.signal_type}`;
    }
    
    // Atualizar timestamp
    document.querySelector('.last-update').textContent = data.last_update;
}

// Iniciar atualização automática
let analysisType = document.body.dataset.analysisType;
if (analysisType) {
    setInterval(() => refreshAnalysis(analysisType), 10000); // Atualizar a cada 10 segundos
}

// Event listeners para filtros e timeframes
document.addEventListener('DOMContentLoaded', function() {
    const timeframeSelector = document.getElementById('timeframe-selector');
    if (timeframeSelector) {
        timeframeSelector.addEventListener('change', function() {
            refreshAnalysis(analysisType);
        });
    }
});