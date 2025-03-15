# Cato 博客系统

Cato 是一个简单、高效的静态博客生成器，灵感来源于 Hexo，但更加轻量级和易于使用。

## 特点

- 🚀 **快速构建** - 高效的构建过程，快速生成静态网站
- 🎨 **多种主题** - 内置多种主题（default、pink、sticky）
- 📱 **响应式设计** - 所有主题都适配移动设备
- 🔌 **简单命令** - 类似 Hexo 的简化命令（如 `cato g`、`cato s`）
- 🛠️ **自定义主题** - 轻松创建和修改自己的主题

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

## 许可证

MIT

## 贡献

欢迎提交 Issues 和 Pull Requests！