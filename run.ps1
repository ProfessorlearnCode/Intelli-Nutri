# run.ps1 - Windows/VS Code friendly PowerShell script

# Step 1: Load .env variables
$envFile = ".env"
if (Test-Path $envFile) {
    $lines = Get-Content $envFile | Where-Object { $_ -notmatch '^#' -and $_ -match '=' }
    foreach ($line in $lines) {
        $parts = $line -split '=', 2
        [System.Environment]::SetEnvironmentVariable($parts[0], $parts[1])
    }
} else {
    Write-Host "⚠️ .env file not found. Please create one with required environment variables." -ForegroundColor Red
    exit 1
}

# Step 2: Check for live-server
$liveServerInstalled = Get-Command "live-server" -ErrorAction SilentlyContinue
if (-not $liveServerInstalled) {
    Write-Host "🧪 live-server not found. Attempting to install it globally..." -ForegroundColor Yellow

    # Check if npm exists
    $npmInstalled = Get-Command "npm" -ErrorAction SilentlyContinue
    if (-not $npmInstalled) {
        Write-Host "❌ npm (Node.js) is not installed. Please install Node.js first." -ForegroundColor Red
        exit 1
    }

    npm install -g live-server

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install live-server. Please try manually." -ForegroundColor Red
        exit 1
    } else {
        Write-Host "✅ live-server installed successfully." -ForegroundColor Green
    }
}

# Step 3: Start frontend
Write-Host "🌐 Starting Frontend (live-server) at http://localhost:$env:FRONTEND_PORT..." -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath "live-server" -ArgumentList "frontend", "--port=$env:FRONTEND_PORT"

# Step 4: Start backend (Flask)
Write-Host "🚀 Starting Backend Flask server at http://localhost:$env:FLASK_PORT..." -ForegroundColor Green
python backend/main.py
