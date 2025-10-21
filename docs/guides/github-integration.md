# GitHub Integration

All templates support automatic GitHub repository creation during project generation.

## Prerequisites

To use this feature, you need:

1. **GitHub CLI (`gh`)** installed
2. **Authenticated** with GitHub

### Installing GitHub CLI

=== "macOS"
    ```bash
    brew install gh
    ```

=== "Linux"
    ```bash
    # Debian/Ubuntu
    sudo apt install gh
    
    # Fedora/RHEL
    sudo dnf install gh
    
    # Arch
    sudo pacman -S github-cli
    ```

=== "Windows"
    ```powershell
    # Using winget
    winget install GitHub.cli
    
    # Using scoop
    scoop install gh
    ```

### Authenticating

After installing, authenticate with GitHub:

```bash
gh auth login
```

Follow the prompts to authenticate via browser or token.

## Using the Feature

When creating a new project, you'll be prompted:

```bash
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/barebone
```

**Prompts:**
```plaintext
create_github_repo [no]: yes
github_username [yourname]: YourGitHubUsername
```

!!! tip "What Happens"
    When you select "yes":
    
    1. ✅ Git repository is initialized
    2. ✅ Initial commit is created
    3. ✅ GitHub repository is created
    4. ✅ Code is pushed to GitHub
    
    All automatically!

## What Gets Created

The hook will:

- Initialize a local git repository
- Create an initial commit with all template files
- Create a public GitHub repository under your username
- Push the initial commit to GitHub
- Display the repository URL

## Example Output

```plaintext
================================================================================
Creating GitHub repository...
================================================================================

📦 Initializing git repository...
✅ Git repository initialized

🚀 Creating repository: YourUsername/my_awesome_project

✅ GitHub repository created successfully!
🔗 Repository URL: https://github.com/YourUsername/my_awesome_project

📤 Initial commit has been pushed to GitHub

================================================================================
✅ Project created successfully!
================================================================================
```

## Options

### Repository Visibility

By default, repositories are created as **public**. To create a private repository, you can modify the hook or create the repo manually first.

### Custom GitHub Username

If your GitHub username differs from your author name, you can specify it:

```bash
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates \
    --directory=templates/barebone \
    github_username=YourActualGitHubUsername
```

## Troubleshooting

### GitHub CLI Not Found

```plaintext
❌ GitHub CLI (gh) is not installed or not in PATH.
```

**Solution:** Install GitHub CLI as shown above.

### Not Authenticated

```plaintext
❌ Not authenticated with GitHub CLI.
```

**Solution:** Run `gh auth login` and complete authentication.

### Repository Already Exists

```plaintext
❌ Error creating repository: already exists
💡 Repository username/project already exists.
```

**Solution:** Either:

- Choose a different project name
- Delete the existing repository on GitHub
- Push manually to the existing repo

### Permission Denied

```plaintext
❌ Error creating repository: HTTP 403
```

**Solution:** Check that:

- You're authenticated: `gh auth status`
- Your token has `repo` permissions
- Re-authenticate if needed: `gh auth login --web`

## Manual Creation

If automatic creation fails, you can still create the repository manually:

```bash
# From your project directory
git init
git add .
git commit -m "Initial commit"

# Create and push to GitHub
gh repo create username/project-name --public --source=. --push
```

## Skipping GitHub Creation

If you don't want to create a GitHub repository:

```bash
# Interactive mode - just select "no"
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates --directory=templates/barebone

# Non-interactive mode
cookiecutter gh:MoustHolmes/cookiecutter-ml-templates \
    --directory=templates/barebone \
    --no-input \
    create_github_repo=no
```

## Best Practices

!!! tip "Repository Setup"
    - Use descriptive repository names
    - Add a good description during template creation
    - Consider adding topics/tags after creation via GitHub web UI
    - Set up branch protection rules for important projects

!!! warning "Private Repositories"
    The default hook creates **public** repositories. For private repos:
    
    ```bash
    # Create repo manually with private flag
    gh repo create username/project-name --private --source=. --push
    ```

## Advanced Usage

### Pre-existing Git Repository

If your project directory is already a git repository, the hook will:

- Skip `git init`
- Create the GitHub repository
- Push to the new remote

### Custom Remote Name

The default remote is `origin`. To use a different name:

```bash
# After template generation
git remote rename origin github
git remote add origin git@your-gitlab.com:user/repo.git
```

## CI/CD Integration

After creating your GitHub repository, you might want to:

1. **Add GitHub Actions** - Templates include basic workflows
2. **Enable Branch Protection** - Protect your main branch
3. **Add Collaborators** - Invite team members
4. **Configure Webhooks** - Set up integrations

```bash
# Add collaborators
gh repo edit --add-collaborator username

# Enable GitHub Pages (if applicable)
gh repo edit --enable-pages

# View repository settings
gh repo view --web
```

## See Also

- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Git Basics](../guides/project-structure.md#version-control)
- [Best Practices](../reference/best-practices.md#version-control)
