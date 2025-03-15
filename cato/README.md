# Cato 静态博客生成器

一个简单易用的静态博客生成器，支持可视化管理界面、Markdown写作、标签管理、分页、RSS订阅等功能。

## 快速开始

1. 安装：
```bash
pip install cato-blog
```

2. 创建博客：
```bash
# 进入你想创建博客的目录
cd your-blog-directory

# 初始化并启动博客
cato init

# 启动开发服务器
cato serve
```

就这么简单！现在你可以访问：
- 博客网站：http://localhost:8000
- 后台管理：http://localhost:8000/admin（默认密码：admin123）

## 功能特点

- 可视化管理界面
  - 文章列表管理
  - Markdown编辑器
  - 标签管理
  - 草稿功能
- Markdown 文章支持
- YAML Front Matter 元数据
- 文章标签系统
- 分页支持
- RSS 订阅
- 实时预览
- 文件监视自动重建
- 响应式设计
- 现代化主题
  - Pink主题：清新可爱的粉色主题
  - Sticky主题：便利贴风格的主题

## 命令行工具

- `cato init`：初始化新博客
- `cato new <title>`：创建新文章
- `cato serve`：启动开发服务器
- `cato build`：构建静态文件
- `cato clean`：清理生成的文件
- `cato deploy`：部署到服务器

## 配置说明

编辑 `config.yml` 文件：

```yaml
# 站点配置
site_name: '我的博客'
site_description: '分享技术与生活'
site_url: 'http://localhost:8000'
author: '博主'
language: 'zh-CN'

# 主题设置
theme: 'default'  # 或 'sticky'

# 分页设置
posts_per_page: 10

# 日期格式
date_format: '%Y-%m-%d'
```

## 目录结构

```
my-blog/
├── config.yml          # 配置文件
├── source/
│   ├── _posts/        # 文章目录
│   └── assets/        # 静态资源
└── public/            # 生成的静态文件
```

## 许可证

MIT License 