// LLM Database Explorer - Frontend Application
// Data sourced from llm_pricing_data.json

const modelsData = [];

// Initialize with pricing data
async function loadModels() {
    try {
        const response = await fetch('llm_pricing_data.json');
        const data = await response.json();
        
        data.providers.forEach(provider => {
            provider.models.forEach(model => {
                modelsData.push({
                    id: model.model_id,
                    name: model.model_id,
                    developer: provider.provider,
                    tags: ["pricing", provider.provider],
                    description: model.description || `${provider.provider} model`,
                    releaseDate: new Date(data.generated_at).toISOString().split('T')[0],
                    contextWindow: model.context_length,
                    inputPricePerMillion: model.input_price_per_million,
                    outputPricePerMillion: model.output_price_per_million
                });
            });
        });
        
        renderModels(modelsData);
    } catch (error) {
        console.error('Failed to load pricing data:', error);
        // Fallback to static data if JSON fails to load
        fallbackData();
    }
}

function fallbackData() {
    // Static fallback data
    const staticData = [
        {
            id: "gpt-4o",
            name: "GPT-4o",
            developer: "OpenAI",
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
            tags: ["proprietary", "multimodal", "fast"],
            description: "Google's fast multimodal model with 1M context window.",
            releaseDate: "2024-10-22",
            contextWindow: 1048576,
            inputPricePerMillion: 0.1,
            outputPricePerMillion: 0.4
        }
    ];
    
    renderModels(staticData);
}

function renderModels(models) {
    const grid = document.getElementById('modelsGrid');
    grid.innerHTML = '';
    
    models.forEach(model => {
        const card = document.createElement('div');
        card.className = 'model-card';
        card.innerHTML = `
            <h3>${model.name}</h3>
            <p class="developer">${model.developer}</p>
            <div class="tags">
                ${model.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
            <p class="description">${model.description}</p>
            <div class="meta">
                <span>Released: ${model.releaseDate}</span>
                <span>Context: ${model.contextWindow.toLocaleString()}</span>
            </div>
            ${model.inputPricePerMillion !== undefined ? `
            <div class="pricing">
                <span class="price">💰 Input: $${model.inputPricePerMillion}/M</span>
                <span class="price">💰 Output: $${model.outputPricePerMillion}/M</span>
            </div>
            ` : ''}
        `;
        grid.appendChild(card);
    });
    
    updateStats(models);
}

function updateStats(models) {
    document.getElementById('totalCount').textContent = models.length;
    const categories = new Set(models.flatMap(m => m.tags));
    document.getElementById('categoryCount').textContent = categories.size;
}

function searchModels(query) {
    const filtered = modelsData.filter(model => 
        model.name.toLowerCase().includes(query.toLowerCase()) ||
        model.developer.toLowerCase().includes(query.toLowerCase()) ||
        model.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
    );
    renderModels(filtered);
}

// Event Listeners
document.getElementById('searchBtn').addEventListener('click', () => {
    const query = document.getElementById('searchInput').value;
    searchModels(query);
});

document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const query = e.target.value;
        searchModels(query);
    }
});

// Load models on startup
loadModels();