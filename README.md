# LLM Database Explorer

A web application to compare pricing and specifications across major AI model providers.

## Features

- **Search**: Full-text search across model names, providers, tags, and descriptions
- **Provider Filter**: Filter by AI model provider (OpenAI, Anthropic, Google, Mistral)
- **Model Type Filter**: Filter by model type (General, Reasoning, Code, Multimodal)
- **Price Range Filter**: Set minimum/maximum input and output prices per million tokens
- **Context Length Filter**: Filter by minimum context window size
- **Sorting**: Sort by input or output price (ascending/descending)

## Usage

1. Open `index.html` in a web browser
2. Use the search bar to find models by name, provider, or tag
3. Use dropdown filters to narrow by provider, model type, and context length
4. Enter price ranges to filter by cost
5. Click "Clear Filters" to reset all filters

## Files

- `index.html` - Main HTML structure
- `app.js` - JavaScript application logic
- `styles.css` - Styling
- `llm_pricing_data.json` - Model pricing data (19 models)

## Data

Currently includes 19 models from 4 providers:
- OpenAI (4 models)
- Anthropic (3 models)
- Google (3 models)
- Mistral (3 models)