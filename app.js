// LLM Database Explorer - Frontend Application
// Enhanced with multiple filter dimensions

const modelsData = [];
let filteredData = [];

// Initialize with pricing data
async function loadModels() {
    try {
        const response = await fetch('llm_pricing_data.json');
        const data = await response.json();
        
        data.providers.forEach(provider => {
            provider.models.forEach(model => {
                // Determine model type based on description and name
                const descLower = (model.description || '').toLowerCase();
                const idLower = (model.model_id || '').toLowerCase();
                
                let modelType = 'general';
                if (idLower.includes('o1') || descLower.includes('reasoning')) {
                    modelType = 'reasoning';
                } else if (idLower.includes('code') || descLower.includes('code generation')) {
                    modelType = 'code';
                } else if (descLower.includes('multimodal')) {
                    modelType = 'multimodal';
                }
                
                modelsData.push({
                    id: model.model_id,
                    name: model.model_id,
                    developer: provider.provider,
                    modelType: modelType,
                    tags: ["pricing", provider.provider.toLowerCase(), modelType],
                    description: model.description || `${provider.provider} model`,
                    releaseDate: new Date(data.generated_at).toISOString().split('T')[0],
                    contextWindow: model.context_length,
                    inputPricePerMillion: model.input_price_per_million,
                    outputPricePerMillion: model.output_price_per_million
                });
            });
        });
        
        populateFilters();
        filteredData = [...modelsData];
        renderModels(filteredData);
        updateStats(filteredData);
    } catch (error) {
        console.error('Failed to load pricing data:', error);
        fallbackData();
    }
}

function populateFilters() {
    // Provider filter
    const providerSelect = document.getElementById('providerFilter');
    const providers = [...new Set(modelsData.map(m => m.developer))].sort();
    providers.forEach(provider => {
        const option = document.createElement('option');
        option.value = provider;
        option.textContent = provider;
        providerSelect.appendChild(option);
    });
    
    // Model type filter
    const typeSelect = document.getElementById('modelTypeFilter');
    const types = ['general', 'reasoning', 'code', 'multimodal'];
    types.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type.charAt(0).toUpperCase() + type.slice(1);
        typeSelect.appendChild(option);
    });
    
    // Context options
    const contextSelect = document.getElementById('contextFilter');
    const contexts = [0, 32000, 128000, 200000, 1048576];
    contexts.forEach(ctx => {
        const option = document.createElement('option');
        option.value = ctx;
        option.textContent = ctx === 0 ? 'Any' : ctx >= 1000000 ? `${ctx/1000000}M+` : `${ctx/1000}K+`;
        contextSelect.appendChild(option);
    });
}

function fallbackData() {
    const staticData = [
        {
            id: "gpt-4o",
            name: "GPT-4o",
            developer: "OpenAI",
            modelType: "multimodal",
            tags: ["proprietary", "multimodal", "reasoning"],
            description: "Advanced reasoning model with improved accuracy and safety.",
            releaseDate: "2023-03-14",
            contextWindow: 128000,
            inputPricePerMillion: 2.5,
            outputPricePerMillion: 10.0
        },
        {
            id: "claude-3-opus",
            name: "Claude 3 Opus",
            developer: "Anthropic",
            modelType: "general",
            tags: ["proprietary", "reasoning", "long-context"],
            description: "Most capable Claude model for complex tasks.",
            releaseDate: "2024-02-08",
            contextWindow: 200000,
            inputPricePerMillion: 15.0,
            outputPricePerMillion: 75.0
        },
        {
            id: "gemini-2.0-flash",
            name: "Gemini 2.0 Flash",
            developer: "Google",
            modelType: "multimodal",
            tags: ["proprietary", "multimodal", "fast"],
            description: "Google's fast multimodal model with 1M context window.",
            releaseDate: "2024-10-22",
            contextWindow: 1048576,
            inputPricePerMillion: 0.1,
            outputPricePerMillion: 0.4
        }
    ];
    
    populateFilters();
    filteredData = [...staticData];
    renderModels(filteredData);
    updateStats(filteredData);
}

function getFilteredData() {
    const searchQuery = document.getElementById('searchInput').value.toLowerCase();
    const provider = document.getElementById('providerFilter').value;
    const modelType = document.getElementById('modelTypeFilter').value;
    const minInputPrice = parseFloat(document.getElementById('minInputPrice').value) || 0;
    const maxInputPrice = parseFloat(document.getElementById('maxInputPrice').value) || Infinity;
    const minOutputPrice = parseFloat(document.getElementById('minOutputPrice').value) || 0;
    const maxOutputPrice = parseFloat(document.getElementById('maxOutputPrice').value) || Infinity;
    const minContext = parseInt(document.getElementById('contextFilter').value) || 0;
    
    let result = modelsData.filter(model => {
        // Search filter
        const matchesSearch = !searchQuery || 
            model.name.toLowerCase().includes(searchQuery) ||
            model.developer.toLowerCase().includes(searchQuery) ||
            model.tags.some(tag => tag.toLowerCase().includes(searchQuery)) ||
            model.description.toLowerCase().includes(searchQuery);
        
        // Provider filter
        const matchesProvider = !provider || model.developer === provider;
        
        // Model type filter
        const matchesType = !modelType || model.modelType === modelType;
        
        // Price range filter
        const matchesInputPrice = 
            (model.inputPricePerMillion || 0) >= minInputPrice &&
            (model.inputPricePerMillion || 0) <= maxInputPrice;
        
        const matchesOutputPrice =
            (model.outputPricePerMillion || 0) >= minOutputPrice &&
            (model.outputPricePerMillion || 0) <= maxOutputPrice;
        
        // Context filter
        const matchesContext = model.contextWindow >= minContext;
        
        return matchesSearch && matchesProvider && matchesType && 
               matchesInputPrice && matchesOutputPrice && matchesContext;
    });
    
    // Price sorting (default: input price ascending)
    const priceSort = document.getElementById('priceSort').value;
    if (priceSort === 'input-asc') {
        result.sort((a, b) => (a.inputPricePerMillion || 0) - (b.inputPricePerMillion || 0));
    } else if (priceSort === 'input-desc') {
        result.sort((a, b) => (b.inputPricePerMillion || 0) - (a.inputPricePerMillion || 0));
    } else if (priceSort === 'output-asc') {
        result.sort((a, b) => (a.outputPricePerMillion || 0) - (b.outputPricePerMillion || 0));
    } else if (priceSort === 'output-desc') {
        result.sort((a, b) => (b.outputPricePerMillion || 0) - (a.outputPricePerMillion || 0));
    }
    
    return result;
}

function renderModels(models) {
    const grid = document.getElementById('modelsGrid');
    grid.innerHTML = '';
    
    if (models.length === 0) {
        grid.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1;">
                <h3>No models found</h3>
                <p>Try adjusting your filters or search terms</p>
            </div>
        `;
        return;
    }
    
    models.forEach(model => {
        const card = document.createElement('div');
        card.className = 'model-card';
        
        const inputPrice = model.inputPricePerMillion !== undefined 
            ? `$${model.inputPricePerMillion.toFixed(2)}` 
            : 'N/A';
        const outputPrice = model.outputPricePerMillion !== undefined 
            ? `$${model.outputPricePerMillion.toFixed(2)}` 
            : 'N/A';
        
        const typeBadge = model.modelType ? 
            `<span class="model-badge type-badge">${model.modelType}</span>` : '';
        
        card.innerHTML = `
            <div class="model-header">
                <div>
                    <div class="model-name">${model.name}</div>
                    <div class="model-developer">${model.developer}</div>
                </div>
                <div class="badges">${typeBadge}<span class="model-badge">${model.tags[1] || 'general'}</span></div>
            </div>
            <p class="model-description">${model.description}</p>
            <div class="model-meta">
                <div class="meta-item">
                    <span class="meta-label">Context</span>
                    <span class="meta-value">${model.contextWindow.toLocaleString()}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Released</span>
                    <span class="meta-value">${model.releaseDate}</span>
                </div>
            </div>
            ${model.inputPricePerMillion !== undefined ? `
            <div class="model-pricing">
                <div class="price-item">
                    <div class="price-label">Input /M</div>
                    <div class="price-value">${inputPrice}</div>
                </div>
                <div class="price-item">
                    <div class="price-label">Output /M</div>
                    <div class="price-value">${outputPrice}</div>
                </div>
            </div>
            ` : ''}
        `;
        grid.appendChild(card);
    });
    
    updateStats(models);
}

function updateStats(models) {
    document.getElementById('totalCount').textContent = models.length;
    
    const providers = new Set(models.map(m => m.developer));
    document.getElementById('providerCount').textContent = providers.size;
    
    const pricedModels = models.filter(m => m.inputPricePerMillion !== undefined);
    if (pricedModels.length > 0) {
        const avgPrice = pricedModels.reduce((sum, m) => sum + (m.inputPricePerMillion || 0), 0) / pricedModels.length;
        document.getElementById('avgInputPrice').textContent = `$${avgPrice.toFixed(2)}`;
    } else {
        document.getElementById('avgInputPrice').textContent = 'N/A';
    }
}

function applyFilters() {
    filteredData = getFilteredData();
    renderModels(filteredData);
}

function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('providerFilter').value = '';
    document.getElementById('modelTypeFilter').value = '';
    document.getElementById('minInputPrice').value = '';
    document.getElementById('maxInputPrice').value = '';
    document.getElementById('minOutputPrice').value = '';
    document.getElementById('maxOutputPrice').value = '';
    document.getElementById('contextFilter').value = '';
    document.getElementById('priceSort').value = '';
    filteredData = [...modelsData];
    renderModels(filteredData);
}

// Event Listeners
document.getElementById('searchBtn').addEventListener('click', applyFilters);
document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') applyFilters();
});

document.getElementById('providerFilter').addEventListener('change', applyFilters);
document.getElementById('modelTypeFilter').addEventListener('change', applyFilters);
document.getElementById('minInputPrice').addEventListener('input', applyFilters);
document.getElementById('maxInputPrice').addEventListener('input', applyFilters);
document.getElementById('minOutputPrice').addEventListener('input', applyFilters);
document.getElementById('maxOutputPrice').addEventListener('input', applyFilters);
document.getElementById('contextFilter').addEventListener('change', applyFilters);
document.getElementById('priceSort').addEventListener('change', applyFilters);
document.getElementById('clearBtn').addEventListener('click', clearFilters);

// Load models on startup
loadModels();
