# 将 Cato 博客系统发布到 GitHub 的指南

本指南将帮助您将 Cato 博客系统发布到 GitHub，以便其他用户可以通过一行命令安装和使用它。

## 1. 准备工作

在开始之前，请确保您已经：

- 安装了 Git
- 拥有 GitHub 账号
- 已经完成了 Cato 博客系统的开发和测试

## 2. 创建 GitHub 仓库

1. 登录您的 GitHub 账号
2. 点击右上角的 "+" 图标，选择 "New repository"
3. 填写仓库名称，例如 "cato-blog"
4. 添加描述："一个简单、高效的静态博客生成器"
5. 选择 "Public" 可见性
6. 勾选 "Add a README file"
7. 点击 "Create repository"

## 3. 克隆仓库到本地

```bash
git clone https://github.com/Jeffrey-done/cato-blog.git
cd cato-blog
```

## 4. 准备文件

1. 将 Cato 博客系统的所有文件复制到克隆的仓库目录中
2. 确保包含以下文件：
   - `setup.py`
   - `cato/` 目录（包含所有源代码）
   - `README.md`
   - `install_cato_minimal.ps1`（一行命令安装脚本）
   - 其他必要的文件

## 5. 更新安装脚本中的 URL

编辑 `install_cato_minimal.ps1` 文件，确保 GitHub URL 正确：

```powershell
# 将此行
Invoke-WebRequest -Uri "https://github.com/Jeffrey-done/cato-blog/archive/refs/heads/master.zip" -OutFile "cato.zip"

# 替换为您的实际 GitHub 用户名
Invoke-WebRequest -Uri "https://github.com/Jeffrey-done/cato-blog/archive/refs/heads/master.zip" -OutFile "cato.zip"
```

## 6. 提交并推送到 GitHub

```bash
git add .
git commit -m "初始提交：Cato 博客系统"
git push origin master
```

## 7. 创建发布版本（可选）

1. 在 GitHub 仓库页面，点击 "Releases"
2. 点击 "Create a new release"
3. 填写版本号，例如 "v1.0.0"
4. 添加发布标题和描述
5. 点击 "Publish release"

## 8. 更新一行命令安装指令

在 README.md 中，确保一行命令安装指令使用正确的 URL：

```powershell
irm https://raw.githubusercontent.com/Jeffrey-done/cato-blog/master/install_cato_minimal.ps1 | iex
```

## 9. 测试安装脚本

在一个全新的环境中测试安装脚本，确保它能正常工作：

```powershell
irm https://raw.githubusercontent.com/Jeffrey-done/cato-blog/master/install_cato_minimal.ps1 | iex
```

## 10. 宣传您的项目

- 在社交媒体上分享您的项目
- 在相关论坛和社区发布介绍
- 创建演示视频并分享
- 撰写博客文章介绍 Cato 的特点和使用方法

## 11. 维护和更新

- 定期检查 Issues 和 Pull Requests
- 修复 bug 和添加新功能
- 更新文档和示例
- 发布新版本

## 常见问题解答

### Q: 用户报告安装失败，如何排查？

A: 请检查以下几点：
- 确保安装脚本中的 URL 正确
- 确保仓库是公开的
- 检查用户的 PowerShell 版本（需要 PowerShell 5.0 或更高版本）
- 检查用户是否有足够的权限安装 Python 包

### Q: 如何更新已发布的版本？

A: 修改代码后，提交并推送到 GitHub，然后创建一个新的发布版本。用户可以使用相同的一行命令安装最新版本。

### Q: 如何处理用户的功能请求？

A: 在 GitHub Issues 中跟踪功能请求，根据优先级和可行性进行开发。与用户保持沟通，让他们了解开发进度。 