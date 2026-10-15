// LLM Pricing Database - Frontend Application
const modelsData = [];
let activeFilter = 'all';

async function loadModels() {
    try {
        const response = await fetch('llm_pricing_data.json');
        const data = await response.json();
        
        data.providers.forEach(provider => {
            provider.models.forEach(model => {
                modelsData.push({
                    id: model.model_id,
                    name: model.model_id,
                    provider: provider.provider,
                    description: model.description || `${provider.provider} model`,
                    contextWindow: model.context_length,
                    inputPrice: model.input_price_per_million,
                    outputPrice: model.output_price_per_million,
                    timestamp: data.generated_at
                });
            });
        });
        
        initFilters();
        renderModels(modelsData);
        updateStats();
    } catch (error) {
        console.error('Failed to load data:', error);
        document.getElementById('modelsGrid').innerHTML = 
            '<div class="no-results"><h3>Failed to load data</h3><p>Please check the JSON file</p></div>';
    }
}

function initFilters() {
    const providers = [...new Set(modelsData.map(m => m.provider))];
    const filterGroup = document.getElementById('filterGroup');
    
    providers.forEach(provider => {
        const btn = document.createElement('button');
        btn.className = 'filter-btn';
        btn.dataset.filter = provider;
        btn.textContent = provider;
        filterGroup.appendChild(btn);
    });
    
    filterGroup.addEventListener('click', (e) => {
        if (e.target.classList.contains('filter-btn')) {
            filterGroup.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            activeFilter = e.target.dataset.filter;
            applyFilters();
        }
        });
}

function applyFilters() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    let filtered = modelsData;
    
    if (activeFilter !== 'all') {
        filtered = filtered.filter(m => m.provider === activeFilter);
    }
    
    if (searchTerm) {
        filtered = filtered.filter(m => 
            m.name.toLowerCase().includes(searchTerm) || 
            m.provider.toLowerCase().includes(searchTerm) ||
            m.description.toLowerCase().includes(searchTerm)
        );
    }
    
    renderModels(filtered);
    updateStats(filtered);
}

function renderModels(models) {
    const grid = document.getElementById('modelsGrid');
    
    if (models.length === 0) {
        grid.innerHTML = '<div class="no-results"><h3>No models found</h3><p>Try adjusting your search or filters</p></div>';
        return;
    }
    
    grid.innerHTML = models.map(model => `
        <div class="model-card">
            <div class="card-header">
                <div class="model-name">${model.name}</div>
                <span class="provider-badge">${model.provider}</span>
            </div>
            <p class="model-desc">${model.description}</p>
            <div class="model-meta">
                <div class="meta-item">
                    <span class="meta-label">Context</span>
                    <span class="meta-value">${formatNumber(model.contextWindow)}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Input ($/M)</span>
                    <span class="meta-value price-highlight">${model.inputPrice.toFixed(2)}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Output ($/M)</span>
                    <span class="meta-value">${model.outputPrice.toFixed(2)}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Ratio</span>
                    <span class="meta-value">${(model.outputPrice / model.inputPrice).toFixed(1)}x</span>
                </div>
            </div>
        </div>
    `).join('');
}

function updateStats(models = modelsData) {
    document.getElementById('totalCount').textContent = models.length;
    const providers = new Set(models.map(m => m.provider));
    document.getElementById('providerCount').textContent = providers.size;
    
    const date = new Date(models[0]?.timestamp || Date.now());
    document.getElementById('lastUpdated').textContent = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(0) + 'K';
    return num.toString();
}

// Event listeners
document.getElementById('searchInput').addEventListener('input', applyFilters);

// Initialize
loadModels();
