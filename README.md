# Cato 博客系统

Cato 是一个简单、高效的静态博客生成器，灵感来源于 Hexo，但更加轻量级和易于使用。

## 特点

- 🚀 **快速构建** - 高效的构建过程，快速生成静态网站
- 🎨 **多种主题** - 内置多种主题（default、pink、sticky）
- 📱 **响应式设计** - 所有主题都适配移动设备
- 🔌 **简单命令** - 类似 Hexo 的简化命令（如 `cato g`、`cato s`）
- 🛠️ **自定义主题** - 轻松创建和修改自己的主题
- 📦 **双分支管理** - master分支用于展示，blog分支存储源文件
- 🔄 **一键恢复** - 支持从blog分支快速恢复源文件
- 🤖 **自动部署** - 支持GitHub Actions自动部署，从blog分支更新到master分支

## 快速安装

### 一行命令安装（推荐）

```powershell
irm https://raw.githubusercontent.com/Jeffrey-done/cato-blog/master/install_cato_minimal.ps1 | iex
```

### 手动安装

1. 克隆仓库
```bash
git clone https://github.com/Jeffrey-done/cato-blog.git
cd cato-blog
```

2. 安装包
```bash
pip install -e .
```

## 使用方法

### 创建新博客

```bash
cato init myblog
cd myblog
```

### 创建新文章

```bash
cato new "我的第一篇文章"
# 或使用简化命令
cato n "我的第一篇文章"
```

### 构建网站

```bash
cato build
# 或使用简化命令
cato g
```

### 启动本地服务器

```bash
cato serve
# 或使用简化命令
cato s
```

### 清理缓存

```bash
cato clean
# 或使用简化命令
cato c
```

### 部署博客

#### 部署展示页面（GitHub Pages）
```bash
cato deploy
# 或使用简化命令
cato d
```
这会将构建后的文件（public目录内容）推送到 master 分支。

#### 部署源文件（用于备份或多设备同步）
```bash
cato deploy-source
# 或使用简化命令
cato ds
```
这会将所有源文件推送到 blog 分支，包括：
- source/ 目录（文章和主题）
- config.yml
- 其他配置文件

### 恢复博客文件
如果你需要恢复之前的博客文件（比如在新设备上或系统更新后），可以使用：
```bash
cato restore
# 或使用简化命令
cato r
```
这个命令会：
1. 自动备份当前文件（以防万一）
2. 从 blog 分支恢复所有源文件
3. 保持构建后的文件不变

## 自动部署功能

除了手动部署外，Cato博客系统还支持通过GitHub Actions自动部署：

### 自动部署设置

1. 确保您的仓库已经设置好blog分支（存储源文件）和master分支（展示网站）
2. 在blog分支创建`.github/workflows/auto-deploy.yml`文件
3. 将以下内容复制到该文件中：

```yaml
name: 智能更新博客

on:
  push:
    branches:
      - blog

permissions:
  contents: write

jobs:
  update-blog:
    runs-on: ubuntu-latest
    steps:
      - name: 检出blog分支
        uses: actions/checkout@v3
        with:
          ref: blog
          
      - name: 安装Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.10'
          
      - name: 安装依赖
        run: |
          python -m pip install --upgrade pip
          pip install markdown pyyaml beautifulsoup4
          
      - name: 生成文章
        run: |
          python process_blog.py
          
      - name: 检出master分支
        uses: actions/checkout@v3
        with:
          ref: master
          path: master-website
          
      - name: 智能更新网站
        run: |
          # 复制新文章到posts目录
          mkdir -p master-website/posts
          cp -n html_articles/*.html master-website/posts/ || echo "没有新文章"
          
          # 智能更新首页
          cp master-website/index.html master-website/index.html.backup
          python update_index.py master-website/index.html html_articles/article_list.html master-website/index.html
          
      - name: 提交到master分支
        run: |
          cd master-website
          git config user.name "GitHub Action"
          git config user.email "action@github.com"
          git add posts/ index.html
          
          if git diff --staged --quiet; then
            echo "没有变更需要提交"
          else
            git commit -m "更新博客 [自动部署]"
            git push
            echo "已更新博客内容"
          fi
```

4. 添加辅助脚本：在blog分支添加`process_blog.py`和`update_index.py`文件
5. 仓库设置：进入GitHub仓库的"Settings" > "Actions" > "General"，在"Workflow permissions"部分选择"Read and write permissions"并保存

### 自动部署工作原理

当您推送内容到blog分支时：

1. GitHub Actions自动触发
2. 系统会检出blog分支，处理所有Markdown文章并生成HTML文件
3. 然后检出master分支，并将新生成的文章和更新的首页添加到master分支
4. 智能首页更新算法会保留原有网站的外观和样式，只更新文章列表部分
5. 最后将变更推送到master分支，完成自动部署

这种方式特别适合使用Cato移动应用（cato-uni-app）撰写和管理博客内容的用户。

## 分支说明

博客使用两个分支管理不同用途的文件：

- **master 分支**：只包含构建后的文件，用于 GitHub Pages 展示
  - 使用 `cato d` 命令更新
  - 只包含 public 目录中的文件

- **blog 分支**：包含所有源文件，用于备份和多设备同步
  - 使用 `cato ds` 命令更新
  - 包含所有源文件（文章、配置、主题等）
  - 用于恢复博客内容

## 主题切换

在 `config.yml` 文件中修改主题设置：

```yaml
# 主题设置
theme: 'default'  # 可选值: default, pink, sticky, custom
```

## 自定义主题

1. 在 `config.yml` 中设置 `theme: 'custom'`
2. 修改 `source/_templates/themes/custom` 目录下的文件

## 目录结构

```
myblog/
├── config.yml          # 配置文件
├── source/             # 源文件目录
│   ├── _posts/         # 文章目录
│   ├── _drafts/        # 草稿目录
│   ├── _templates/     # 模板目录
│   │   └── themes/     # 主题目录
│   │       ├── default/# 默认主题
│   │       ├── pink/   # 粉色主题
│   │       ├── sticky/ # 便签主题
│   │       └── custom/ # 自定义主题
│   └── assets/         # 资源文件
└── public/             # 生成的静态文件
```

## 系统更新

### 更新博客系统
```bash
pip install --upgrade cato-blog
# 或从 GitHub 安装最新版本
pip install --upgrade git+https://github.com/Jeffrey-done/cato-blog.git
```

### 更新后恢复文件
如果系统更新后需要恢复原来的文件：
```bash
cato r  # 从 blog 分支恢复所有源文件
```

## 许可证

MIT

## 贡献

欢迎提交 Issues 和 Pull Requests！