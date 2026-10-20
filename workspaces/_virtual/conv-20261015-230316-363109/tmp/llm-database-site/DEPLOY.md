# Deployment Instructions

## Manual Git Initialization (Requires :grant danger)

```powershell
cd C:\Users\User\AppData\Local\SMS\workspaces\_virtual\conv-20261015-230316-363109\tmp\llm-database-site
git init
git add .
git commit -m "Initial commit: LLM Database Explorer"
```

## Create GitHub Repository

```powershell
gh repo create llm-database-explorer --public --push --source=. --remote=origin
```

Or manually at https://github.com/new

## Enable GitHub Pages

1. Go to repository Settings
2. Navigate to Pages
3. Select `main` branch and `/ (root)` folder
4. Click Save

## Automation

The `.github/workflows/deploy.yml` file will automatically deploy when you push to main.

## Verification

After deployment, visit: https://[your-username].github.io/llm-database-explorer