# Cato 博客系统一键安装脚本
# 作者：Jeffrey-done
# 版本：1.0.0

Write-Host "开始安装 Cato 博客系统..." -ForegroundColor Cyan

# 检查 Python 是否已安装
try {
    $pythonVersion = python --version
    Write-Host "检测到 Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "未检测到 Python，请先安装 Python 3.6 或更高版本" -ForegroundColor Red
    Write-Host "您可以从 https://www.python.org/downloads/ 下载 Python" -ForegroundColor Yellow
    exit 1
}

# 检查 pip 是否已安装
try {
    $pipVersion = pip --version
    Write-Host "检测到 pip: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "未检测到 pip，正在安装..." -ForegroundColor Yellow
    Invoke-Expression "python -m ensurepip --upgrade"
}

# 创建临时目录
$tempDir = Join-Path $env:TEMP "cato-install"
if (Test-Path $tempDir) {
    Remove-Item -Path $tempDir -Recurse -Force
}
New-Item -Path $tempDir -ItemType Directory | Out-Null
Set-Location $tempDir

Write-Host "正在下载 Cato 博客系统..." -ForegroundColor Cyan

# 从 GitHub 克隆仓库
try {
    Invoke-Expression "git clone https://github.com/Jeffrey-done/cato-blog.git ."
} catch {
    # 如果 git 不可用，则使用 PowerShell 下载 ZIP 文件
    $zipUrl = "https://github.com/Jeffrey-done/cato-blog/archive/refs/heads/master.zip"
    $zipFile = Join-Path $tempDir "cato-blog.zip"
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile
    Expand-Archive -Path $zipFile -DestinationPath $tempDir
    Get-ChildItem -Path (Join-Path $tempDir "cato-blog-master") -Recurse | Move-Item -Destination $tempDir
    Remove-Item -Path (Join-Path $tempDir "cato-blog-master") -Recurse -Force
    Remove-Item -Path $zipFile -Force
}

Write-Host "正在安装 Cato 博客系统..." -ForegroundColor Cyan

# 安装 Cato 博客系统
try {
    Invoke-Expression "pip install -e ."
    Write-Host "Cato 博客系统安装成功！" -ForegroundColor Green
} catch {
    Write-Host "安装失败: $_" -ForegroundColor Red
    exit 1
}

# 创建示例博客
$blogDir = Read-Host "请输入您想要创建博客的目录名称 (默认: myblog)"
if ([string]::IsNullOrEmpty($blogDir)) {
    $blogDir = "myblog"
}

try {
    # 返回到原始目录
    Set-Location $PSScriptRoot
    
    # 创建博客目录
    if (!(Test-Path $blogDir)) {
        New-Item -Path $blogDir -ItemType Directory | Out-Null
    }
    
    # 初始化博客
    Set-Location $blogDir
    Invoke-Expression "cato init ."
    
    Write-Host "博客创建成功！" -ForegroundColor Green
    Write-Host "您可以通过以下命令启动博客服务器：" -ForegroundColor Yellow
    Write-Host "cd $blogDir" -ForegroundColor Yellow
    Write-Host "cato serve" -ForegroundColor Yellow
    
    $startServer = Read-Host "是否现在启动博客服务器？(y/n)"
    if ($startServer -eq "y") {
        Invoke-Expression "cato serve"
    }
} catch {
    Write-Host "创建博客失败: $_" -ForegroundColor Red
    exit 1
} 