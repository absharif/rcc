# GitHub Setup Instructions

## Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the repository details:
   - **Repository name**: `city-corporation-management` (or your preferred name)
   - **Description**: "Django-based City Corporation Management System with premium UI"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these commands:

```bash
# Add the remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

## Alternative: Using SSH (if you have SSH keys set up)

```bash
git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 3: Verify

1. Go to your GitHub repository page
2. You should see all your files uploaded
3. The README.md will be displayed on the repository homepage

## Important Notes

⚠️ **Security Warning**: The `SECRET_KEY` in `settings.py` is currently visible in the repository. For production:
- Use environment variables
- Never commit sensitive keys to public repositories
- Consider using `python-decouple` or `django-environ` for managing secrets

## Future Updates

To push future changes:

```bash
git add .
git commit -m "Your commit message"
git push
```

## Repository Structure

Your repository includes:
- ✅ All Django apps and models
- ✅ Custom admin dashboard
- ✅ Premium UI templates
- ✅ Static files and CSS
- ✅ Requirements.txt
- ✅ README.md
- ✅ .gitignore (excludes venv, db.sqlite3, etc.)
