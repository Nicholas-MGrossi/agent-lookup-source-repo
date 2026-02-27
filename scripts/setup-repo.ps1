param(
  [string]$remote = "",
  [string]$name = "",
  [string]$email = ""
)

# Basic setup script to initialize repo, create main branch, commit, and optionally add remote.
# Usage: .\scripts\setup-repo.ps1 -remote "git@..." -name "Your Name" -email "you@example.com"

function Check-Command($cmd){
    $p = Get-Command $cmd -ErrorAction SilentlyContinue
    return $null -ne $p
}

if (-not (Check-Command git)){
    Write-Host "git is not installed or not on PATH. Please install Git (https://git-scm.com/) and re-run this script." -ForegroundColor Yellow
    exit 1
}

if ($name -ne "") { git config user.name "$name" }
if ($email -ne "") { git config user.email "$email" }

# Initialize if not a git repo
if (-not (Test-Path ".git")){
    git init -b main
    Write-Host "Initialized empty git repo on branch 'main'"
} else {
    Write-Host "Repository already initialized"
}

git add .
if (-not (git rev-parse --verify HEAD 2>$null)){
    git commit -m "chore: initial project files"
} else {
    git commit -m "chore: update files" || Write-Host "No changes to commit"
}

if ($remote -ne ""){
    git remote add origin $remote 2>$null || (git remote set-url origin $remote)
    Write-Host "Set remote 'origin' to $remote"
}

Write-Host "Setup complete. Run 'git push -u origin main' to push (if remote added)." -ForegroundColor Green
