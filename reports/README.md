# Test Reports Publishing System

This system allows automatic publishing of test reports to GitHub Pages in two ways:
1. Automatically through GitHub Actions
2. Manually through a local script

## GitHub Pages Configuration

1. Go to repository settings
2. Select Pages from the left menu
3. Under "Build and deployment":
   - Source: select "GitHub Actions"
   - Branch: select "main"
4. Save configuration

## Method 1: Using GitHub Actions

GitHub Actions will automatically publish reports when there is a push to the `reports/` directory on the main branch.
The workflow file is configured at `.github/workflows/publish-reports.yml`

## Method 2: Using Local Script

### Prerequisites

1. Ensure Python 3.x is installed
2. Configure git user.name and user.email (script will prompt if not configured)

### Usage

To publish a report: