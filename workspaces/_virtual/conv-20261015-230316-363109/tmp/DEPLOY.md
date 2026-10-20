# GitHub Pages Deployment Guide

## Prerequisites

- GitHub account
- Git installed locally

## Quick Deploy

1. **Initialize Git repository:**
   ```bash
   cd llm-database-site
   git init
   git add .
   git commit -m "Initial commit: LLM Database site"
   ```

2. **Create GitHub repository:**
   - Go to https://github.com/new
   - Repository name: `llm-database`
   - Make it public
   - Click "Create repository"

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/llm-database.git
   git branch -M main
   git push -u origin main
   ```

4. **Enable GitHub Pages:**
   - Go to repository Settings
   - Navigate to Pages section
   - Source: Deploy from a branch
   - Branch: `main` / `/ (root)`
   - Click Save

5. **Access your site:**
   - URL: `https://YOUR_USERNAME.github.io/llm-database/`

## Automatic Deployment with GitHub Actions

A workflow file `.github/workflows/deploy.yml` is included for automatic deployment on every push to `main`.

### Workflow Features:
- Automatically builds and deploys on push
- Uses static site deployment
- No build step required (static HTML/CSS/JS)

## Custom Domain (Optional)

To use a custom domain:
1. Add a `CNAME` file with your domain name
2. Configure DNS records at your domain registrar
3. Enable HTTPS in GitHub Pages settings

## Updating Content

To update the LLM data:
1. Edit `data/llm_database.json`
2. Commit and push changes
3. GitHub Actions will automatically redeploy

## Local Testing

```bash
# Serve locally with Python
python -m http.server 8080

# Or with Node.js
npx http-server
```

Then visit `http://localhost:8080`
