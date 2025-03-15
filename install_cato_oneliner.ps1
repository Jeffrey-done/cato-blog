# 一行命令安装脚本
# 这个脚本会被托管在 GitHub 上，用户可以通过以下命令运行：
# irm https://raw.githubusercontent.com/Jeffrey-done/cato-blog/master/scripts/install_cato_oneliner.ps1 | iex

# 检查 Python 是否已安装
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "未检测到 Python，请先安装 Python 3.6 或更高版本" -ForegroundColor Red
    Write-Host "您可以从 https://www.python.org/downloads/ 下载 Python" -ForegroundColor Yellow
    exit 1
}

# 创建临时目录
$tempDir = Join-Path $env:TEMP "cato-install"
if (Test-Path $tempDir) { Remove-Item -Path $tempDir -Recurse -Force }
New-Item -Path $tempDir -ItemType Directory | Out-Null
Set-Location $tempDir

# 下载并安装 Cato
Write-Host "正在下载并安装 Cato 博客系统..." -ForegroundColor Cyan
try {
    # 下载 ZIP 文件
    $zipUrl = "https://github.com/Jeffrey-done/cato-blog/archive/refs/heads/master.zip"
    $zipFile = Join-Path $tempDir "cato-blog.zip"
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile
    
    # 解压 ZIP 文件
    Expand-Archive -Path $zipFile -DestinationPath $tempDir
    Set-Location (Join-Path $tempDir "cato-blog-master")
    
    # 安装 Cato
    pip install -e . | Out-Null
    
    Write-Host "Cato 博客系统安装成功！" -ForegroundColor Green
    
    # 询问是否创建博客
    $createBlog = Read-Host "是否创建新博客？(y/n)"
    if ($createBlog -eq "y") {
        $blogDir = Read-Host "请输入博客目录名称 (默认: myblog)"
        if ([string]::IsNullOrEmpty($blogDir)) { $blogDir = "myblog" }
        
        # 返回到用户目录
        Set-Location $HOME
        
        # 创建并初始化博客
        if (!(Test-Path $blogDir)) { New-Item -Path $blogDir -ItemType Directory | Out-Null }
        Set-Location $blogDir
        cato init .
        
        Write-Host "博客创建成功！您可以通过以下命令启动博客服务器：" -ForegroundColor Green
        Write-Host "cd $blogDir" -ForegroundColor Yellow
        Write-Host "cato serve" -ForegroundColor Yellow
        
        $startServer = Read-Host "是否现在启动博客服务器？(y/n)"
        if ($startServer -eq "y") { cato serve }
    }
} catch {
    Write-Host "安装失败: $_" -ForegroundColor Red
    exit 1
} finally {
    # 清理临时文件
    if (Test-Path $tempDir) { Remove-Item -Path $tempDir -Recurse -Force }
} 