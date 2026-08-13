#Requires -RunAsAdministrator
<#
.SYNOPSIS
  Install ART Edge Face as a Windows Service (headless).
.NOTES
  Run on POS: Windows 11, Python 3.10+, Intel iGPU drivers current.
#>
param(
  [string]$InstallDir = "C:\ART\EdgeFace",
  [string]$Python = "python",
  [string]$ConfigSource = ""
)

$ErrorActionPreference = "Stop"

Write-Host "== ART Edge Face install ==" -ForegroundColor Cyan

if (-not (Test-Path $InstallDir)) {
  New-Item -ItemType Directory -Path $InstallDir | Out-Null
}

# Expect repo / release package already copied to InstallDir
Set-Location $InstallDir

& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements.txt
& $Python -m pip install pywin32
& $Python -m pip install -e .

if ($ConfigSource -and (Test-Path $ConfigSource)) {
  Copy-Item $ConfigSource (Join-Path $InstallDir "config.json") -Force
} elseif (-not (Test-Path (Join-Path $InstallDir "config.json"))) {
  Copy-Item (Join-Path $InstallDir "config.example.json") (Join-Path $InstallDir "config.json")
  Write-Host "Created config.json from example — EDIT RTSP / HQ URL before start." -ForegroundColor Yellow
}

$env:EDGE_FACE_CONFIG = Join-Path $InstallDir "config.json"

# Register service via module entry
& $Python -m edge_face install
& $Python -m edge_face start

Write-Host "Service ARTEdgeFace installed & started." -ForegroundColor Green
Write-Host "Logs: $InstallDir\logs\edge_face.log"
Write-Host "Config: $env:EDGE_FACE_CONFIG"
