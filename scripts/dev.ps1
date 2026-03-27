param(
    [Parameter(Mandatory = $true)]
    [ValidateSet(
        "backend",
        "frontend",
        "start-local",
        "start-all",
        "stop-all",
        "restart-all",
        "status",
        "compose-up",
        "health",
        "interview",
        "reset",
        "resume",
        "questions",
        "rag",
        "voice-tts",
        "voice-stt",
        "jd-analyze",
        "jd-generate",
        "jd-upload-analyze",
        "jd-upload-generate",
        "feature-plan"
    )]
    [string]$Command
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$RuntimeDir = Join-Path $Root ".runtime"
$BackendPidFile = Join-Path $RuntimeDir "backend.pid"
$FrontendPidFile = Join-Path $RuntimeDir "frontend.pid"
$BackendOutLog = Join-Path $RuntimeDir "backend.out.log"
$BackendErrLog = Join-Path $RuntimeDir "backend.err.log"
$FrontendOutLog = Join-Path $RuntimeDir "frontend.out.log"
$FrontendErrLog = Join-Path $RuntimeDir "frontend.err.log"

function Ensure-RuntimeDir {
    if (-not (Test-Path $RuntimeDir)) {
        New-Item -ItemType Directory -Path $RuntimeDir | Out-Null
    }
}

function Test-PortOpen {
    param([int]$Port)
    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $async = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
        $ok = $async.AsyncWaitHandle.WaitOne(1000, $false)
        if (-not $ok) {
            $client.Close()
            return $false
        }
        $client.EndConnect($async) | Out-Null
        $client.Close()
        return $true
    }
    catch {
        return $false
    }
}

function Get-TrackedProcess {
    param([string]$PidFile)
    if (-not (Test-Path $PidFile)) {
        return $null
    }

    $pidValue = Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $pidValue) {
        Remove-Item -LiteralPath $PidFile -Force -ErrorAction SilentlyContinue
        return $null
    }

    try {
        return Get-Process -Id ([int]$pidValue) -ErrorAction Stop
    }
    catch {
        Remove-Item -LiteralPath $PidFile -Force -ErrorAction SilentlyContinue
        return $null
    }
}

function Wait-ForPort {
    param(
        [int]$Port,
        [int]$TimeoutSeconds = 20
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if (Test-PortOpen -Port $Port) {
            return $true
        }
        Start-Sleep -Milliseconds 500
    }
    return $false
}

function Start-ManagedProcess {
    param(
        [string]$Name,
        [string]$PidFile,
        [string]$OutLog,
        [string]$ErrLog,
        [int]$Port,
        [string[]]$ArgumentList
    )

    Ensure-RuntimeDir

    if (Test-PortOpen -Port $Port) {
        Write-Output "$Name already listening on port $Port"
        return
    }

    $existing = Get-TrackedProcess -PidFile $PidFile
    if ($existing) {
        try {
            Stop-Process -Id $existing.Id -Force -ErrorAction Stop
            Start-Sleep -Seconds 1
        }
        catch {
        }
    }

    if (Test-Path $OutLog) { Remove-Item -LiteralPath $OutLog -Force -ErrorAction SilentlyContinue }
    if (Test-Path $ErrLog) { Remove-Item -LiteralPath $ErrLog -Force -ErrorAction SilentlyContinue }

    $escapedRoot = $Root.Replace("'", "''")
    $quotedArgs = ($ArgumentList | ForEach-Object {
        if ($_ -match '\s') { '"' + $_.Replace('"', '\"') + '"' } else { $_ }
    }) -join ' '
    $command = "Set-Location -LiteralPath '$escapedRoot'; python $quotedArgs"

    $proc = Start-Process powershell `
        -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', $command) `
        -WorkingDirectory $Root `
        -PassThru `
        -WindowStyle Minimized `
        -RedirectStandardOutput $OutLog `
        -RedirectStandardError $ErrLog

    Set-Content -LiteralPath $PidFile -Value $proc.Id

    if (Wait-ForPort -Port $Port -TimeoutSeconds 20) {
        Write-Output "$Name started on http://127.0.0.1:$Port"
        return
    }

    $stderr = ""
    if (Test-Path $ErrLog) {
        $stderr = Get-Content $ErrLog -Raw -ErrorAction SilentlyContinue
    }
    throw "$Name failed to start on port $Port.`n$stderr"
}

function Stop-ManagedProcess {
    param(
        [string]$Name,
        [string]$PidFile,
        [int]$Port
    )

    $existing = Get-TrackedProcess -PidFile $PidFile
    if ($existing) {
        try {
            Stop-Process -Id $existing.Id -Force -ErrorAction Stop
        }
        catch {
        }
        Remove-Item -LiteralPath $PidFile -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
    }

    if (Test-PortOpen -Port $Port) {
        Write-Output "$Name still appears to be listening on port $Port"
    }
    else {
        Write-Output "$Name stopped"
    }
}

function Show-Status {
    $backendUp = Test-PortOpen -Port 8001
    $frontendUp = Test-PortOpen -Port 8501
    [pscustomobject]@{
        backend_running = $backendUp
        backend_url = "http://127.0.0.1:8001"
        frontend_running = $frontendUp
        frontend_url = "http://127.0.0.1:8501"
        backend_pid = if (Test-Path $BackendPidFile) { (Get-Content $BackendPidFile | Select-Object -First 1).ToString() } else { "" }
        frontend_pid = if (Test-Path $FrontendPidFile) { (Get-Content $FrontendPidFile | Select-Object -First 1).ToString() } else { "" }
        runtime_dir = $RuntimeDir
    } | ConvertTo-Json -Depth 5
}

switch ($Command) {
    "backend" {
        Push-Location $Root
        try {
            python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001
        }
        finally {
            Pop-Location
        }
    }

    "frontend" {
        Push-Location $Root
        try {
            python -m streamlit run frontend/app.py --server.headless true --browser.gatherUsageStats false --server.address 127.0.0.1 --server.port 8501
        }
        finally {
            Pop-Location
        }
    }

    "start-local" {
        $escapedRoot = $Root.Replace("'", "''")
        $backendCommand = "Set-Location -LiteralPath '$escapedRoot'; python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001"
        $frontendCommand = "Set-Location -LiteralPath '$escapedRoot'; python -m streamlit run frontend/app.py --server.headless true --browser.gatherUsageStats false --server.address 127.0.0.1 --server.port 8501"

        Start-Process powershell -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $backendCommand) -WorkingDirectory $Root
        Start-Sleep -Seconds 2
        Start-Process powershell -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-Command', $frontendCommand) -WorkingDirectory $Root

        Write-Output "Backend launching at http://127.0.0.1:8001"
        Write-Output "Frontend launching at http://127.0.0.1:8501"
    }

    "start-all" {
        Start-ManagedProcess -Name "Backend" -PidFile $BackendPidFile -OutLog $BackendOutLog -ErrLog $BackendErrLog -Port 8001 -ArgumentList @('-m', 'uvicorn', 'backend.main:app', '--host', '127.0.0.1', '--port', '8001')
        Start-ManagedProcess -Name "Frontend" -PidFile $FrontendPidFile -OutLog $FrontendOutLog -ErrLog $FrontendErrLog -Port 8501 -ArgumentList @('-m', 'streamlit', 'run', 'frontend/app.py', '--server.headless', 'true', '--browser.gatherUsageStats', 'false', '--server.address', '127.0.0.1', '--server.port', '8501')
        Show-Status
    }

    "stop-all" {
        Stop-ManagedProcess -Name "Frontend" -PidFile $FrontendPidFile -Port 8501
        Stop-ManagedProcess -Name "Backend" -PidFile $BackendPidFile -Port 8001
        Show-Status
    }

    "restart-all" {
        Stop-ManagedProcess -Name "Frontend" -PidFile $FrontendPidFile -Port 8501
        Stop-ManagedProcess -Name "Backend" -PidFile $BackendPidFile -Port 8001
        Start-ManagedProcess -Name "Backend" -PidFile $BackendPidFile -OutLog $BackendOutLog -ErrLog $BackendErrLog -Port 8001 -ArgumentList @('-m', 'uvicorn', 'backend.main:app', '--host', '127.0.0.1', '--port', '8001')
        Start-ManagedProcess -Name "Frontend" -PidFile $FrontendPidFile -OutLog $FrontendOutLog -ErrLog $FrontendErrLog -Port 8501 -ArgumentList @('-m', 'streamlit', 'run', 'frontend/app.py', '--server.headless', 'true', '--browser.gatherUsageStats', 'false', '--server.address', '127.0.0.1', '--server.port', '8501')
        Show-Status
    }

    "status" {
        Show-Status
    }

    "compose-up" {
        Push-Location $Root
        try {
            docker compose up --build
        }
        finally {
            Pop-Location
        }
    }

    "health" {
        Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8001/health" | ConvertTo-Json -Depth 5
    }

    "interview" {
        $body = @{
            message = "Ask me a PM-delivery interview question about execution risk."
        } | ConvertTo-Json
        Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8001/api/interview" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 5
    }

    "reset" {
        Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8001/api/reset" | ConvertTo-Json -Depth 5
    }

    "resume" {
        $body = @{
            text = "Product manager with delivery ownership across roadmap planning, stakeholder management, and release execution."
        } | ConvertTo-Json
        Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8001/api/resume/analyze" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 5
    }

    "rag" {
        Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8001/api/rag/search?q=stakeholder%20management" | ConvertTo-Json -Depth 5
    }

    "questions" {
        $tempFile = Join-Path $env:TEMP "sample_resume.txt"
        Set-Content -Path $tempFile -Value "Product manager with delivery ownership across roadmap planning, stakeholder management, launch readiness, and execution risk management."
        try {
            curl.exe -X POST "http://127.0.0.1:8001/api/resume/questions" -F "file=@$tempFile"
        }
        finally {
            if (Test-Path $tempFile) {
                Remove-Item -LiteralPath $tempFile -Force
            }
        }
    }

    "voice-tts" {
        $body = @{
            text = "Tell me about a delivery tradeoff you handled."
        } | ConvertTo-Json
        Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8001/api/voice/tts" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 5
    }

    "voice-stt" {
        $tempFile = Join-Path $env:TEMP "sample_audio.wav"
        [System.IO.File]::WriteAllBytes($tempFile, [byte[]](0..31))
        try {
            curl.exe -X POST "http://127.0.0.1:8001/api/voice/stt" -F "file=@$tempFile"
        }
        finally {
            if (Test-Path $tempFile) {
                Remove-Item -LiteralPath $tempFile -Force
            }
        }
    }

    "jd-analyze" {
        $body = @{
            text = "Product Manager - Delivery role responsible for cross-functional execution, release planning, stakeholder alignment, KPI tracking, and risk mitigation across multiple teams."
        } | ConvertTo-Json
        Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8001/api/jd/analyze" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 7
    }

    "jd-generate" {
        $body = @{
            text = "Product Manager - Delivery role responsible for cross-functional execution, release planning, stakeholder alignment, KPI tracking, and risk mitigation across multiple teams."
        } | ConvertTo-Json
        Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8001/api/jd/generate-interview" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 7
    }

    "jd-upload-analyze" {
        $tempFile = Join-Path $env:TEMP "sample_jd.txt"
        Set-Content -Path $tempFile -Value "Product Manager - Delivery role responsible for cross-functional execution, release planning, stakeholder alignment, KPI tracking, and risk mitigation across multiple teams."
        try {
            curl.exe -X POST "http://127.0.0.1:8001/api/jd/analyze-upload" -F "file=@$tempFile"
        }
        finally {
            if (Test-Path $tempFile) {
                Remove-Item -LiteralPath $tempFile -Force
            }
        }
    }

    "jd-upload-generate" {
        $tempFile = Join-Path $env:TEMP "sample_jd.txt"
        Set-Content -Path $tempFile -Value "Product Manager - Delivery role responsible for cross-functional execution, release planning, stakeholder alignment, KPI tracking, and risk mitigation across multiple teams."
        try {
            curl.exe -X POST "http://127.0.0.1:8001/api/jd/generate-interview-upload" -F "file=@$tempFile"
        }
        finally {
            if (Test-Path $tempFile) {
                Remove-Item -LiteralPath $tempFile -Force
            }
        }
    }

    "feature-plan" {
        $body = @{
            request = "Add a delivery-risk simulation mode with competency scoring for every answer."
        } | ConvertTo-Json
        Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8001/api/features/plan" -ContentType "application/json" -Body $body | ConvertTo-Json -Depth 7
    }
}
