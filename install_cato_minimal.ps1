# 最小化一行命令安装脚本
# 用户可以通过以下命令运行：
# irm https://raw.githubusercontent.com/Jeffrey-done/cato-blog/master/install_cato_minimal.ps1 | iex

$ErrorActionPreference = 'Stop'
Write-Host "正在安装 Cato 博客系统..." -ForegroundColor Cyan
$tempDir = Join-Path $env:TEMP "cato-install-$(Get-Random)"
New-Item -Path $tempDir -ItemType Directory -Force | Out-Null
Set-Location $tempDir
Invoke-WebRequest -Uri "https://github.com/Jeffrey-done/cato-blog/archive/refs/heads/master.zip" -OutFile "cato.zip"
Expand-Archive -Path "cato.zip" -DestinationPath $tempDir
Set-Location (Get-ChildItem -Directory | Select-Object -First 1)
pip install -e . | Out-Null
Write-Host "Cato 博客系统安装成功！" -ForegroundColor Green
Write-Host "您可以通过以下命令创建新博客：" -ForegroundColor Yellow
Write-Host "cato init myblog" -ForegroundColor Yellow
Write-Host "cd myblog" -ForegroundColor Yellow
Write-Host "cato serve" -ForegroundColor Yellow
Remove-Item -Path $tempDir -Recurse -Force 