#!/bin/bash

# FootyBets.ai GitHub Repository Setup Script
# This script helps you set up the GitHub repository and push your code

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 FootyBets.ai GitHub Repository Setup${NC}"
echo "=================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git not found. Please install Git first.${NC}"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not in a git repository. Please run 'git init' first.${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Current git status:${NC}"
git status --porcelain

echo ""
echo -e "${YELLOW}🔗 GitHub Repository Setup Instructions:${NC}"
echo "=================================================="
echo ""
echo "1. Go to https://github.com/new"
echo "2. Repository name: footybets-ai"
echo "3. Description: AI-powered AFL betting predictions and analysis platform"
echo "4. Make it PUBLIC (for easier Cloud Build integration)"
echo "5. DO NOT initialize with README (we already have files)"
echo "6. Click 'Create repository'"
echo ""
echo -e "${YELLOW}🔐 Authentication Options:${NC}"
echo "=================================================="
echo ""
echo "Option A: Personal Access Token (Recommended)"
echo "1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)"
echo "2. Generate new token with 'repo' permissions"
echo "3. Copy the token"
echo ""
echo "Option B: SSH Keys"
echo "1. Generate SSH key: ssh-keygen -t ed25519 -C 'your-email@example.com'"
echo "2. Add to GitHub: Settings → SSH and GPG keys → New SSH key"
echo ""
echo -e "${GREEN}✅ Once you've created the repository, run:${NC}"
echo "=================================================="
echo ""
echo "For HTTPS (with Personal Access Token):"
echo "git remote set-url origin https://github.com/digitalimprov/footybets-ai.git"
echo "git push -u origin main"
echo ""
echo "For SSH:"
echo "git remote set-url origin git@github.com:digitalimprov/footybets-ai.git"
echo "git push -u origin main"
echo ""
echo -e "${BLUE}🔧 After pushing to GitHub:${NC}"
echo "=================================================="
echo "1. Set up Cloud Build trigger in Google Cloud Console"
echo "2. Connect GitHub repository to Cloud Build"
echo "3. Test automatic deployment by making a small change and pushing"
echo ""
echo -e "${GREEN}🎉 Your FootyBets.ai will then have automatic CI/CD!${NC}" 