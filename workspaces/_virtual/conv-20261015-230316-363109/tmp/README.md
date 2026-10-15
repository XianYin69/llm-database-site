# LLM Database Explorer

A comprehensive web application for exploring and comparing Large Language Models from multiple providers.

## Features

- **Interactive Model Browser**: Search and filter LLM models by provider, price, or features
- **Real-time Comparison**: View pricing, rate limits, and capabilities side-by-side
- **Responsive Design**: Works on desktop and mobile devices
- **Auto-Deployment**: GitHub Actions workflow for continuous deployment
- **Dark Theme**: Modern UI with easy-on-the-eyes design

## Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/llm-database.git
cd llm-database

# Install dependencies (optional for static site)
npm install

# Start development server
python -m http.server 8080
# or
npx http-server
```

Open `http://localhost:8080` in your browser.

### GitHub Pages Deployment

1. **Create a new GitHub repository**
   - Go to https://github.com/new
   - Repository name: `llm-database`
   - Make it public
   - Click "Create repository"

2. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: LLM Database site"
   git remote add origin https://github.com/YOUR_USERNAME/llm-database.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable GitHub Pages**
   - Go to repository Settings
   - Navigate to Pages section
   - Source: Deploy from a branch
   - Branch: `main` / `/ (root)`
   - Click Save

4. **Access your site**
   - URL: `https://YOUR_USERNAME.github.io/llm-database/`

## File Structure

```
llm-database-site/
├── .github/
│   └── workflows/
│       └── deploy.yml    # GitHub Actions CI/CD
├── index.html            # Main HTML file
├── styles.css            # Stylesheet
├── app.js                # Application logic
├── package.json          # Dependencies
├── README.md             # This file
├── DEPLOY.md             # Deployment guide
└── llm_database.json     # LLM data
```

## Model Data

The application includes sample data for popular LLMs:

### OpenAI
- GPT-4o ($2.50/$10.00 per 1M tokens)
- GPT-4o Mini ($0.15/$0.60 per 1M tokens)

### Anthropic
- Claude 3 Opus ($15.00/$75.00 per 1M tokens)
- Claude 3 Sonnet ($3.00/$15.00 per 1M tokens)
- Claude 3 Haiku ($0.25/$1.25 per 1M tokens)

### Google AI
- Gemini 1.5 Pro ($1.25/$5.00 per 1M tokens)
- Gemini 1.5 Flash ($0.075/$0.30 per 1M tokens)

### Mistral AI
- Mistral Large ($2.00/$6.00 per 1M tokens)
- Codestral ($0.30/$0.90 per 1M tokens)

## Customization

### Change Theme Colors

Edit CSS variables in `styles.css`:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --bg-color: #0f172a;
    /* ... */
}
```

### Add More Models

Add entries to the `modelsData` array in `app.js`:

```javascript
{
    id: 7,
    name: "Your Model",
    developer: "Developer Name",
    tags: ["tag1", "tag2"],
    description: "Description here",
    releaseDate: "YYYY-MM-DD",
    contextWindow: 128000
}
```

### Update Provider Data

Edit `llm_database.json` with new pricing or model information.

## API Schema

The JSON data follows this schema:

- `providers[]` — Provider info (id, name, website, api_base, auth_type)
- `models[]` — Model details (pricing, context window, rate limits, capabilities)
- `endpoints[]` — API endpoint configurations

See `llm_registry_schema.json` for the full schema definition.

## License

MIT License - feel free to use and modify.
