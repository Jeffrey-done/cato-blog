import os
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from . import __version__
from .core import BlogBuilder, BlogDevServer

def init_blog(args):
    """初始化博客"""
    try:
        print(f"\n开始在 {args.path} 目录初始化博客...")
        print("-------------------")
        
        # 创建目标目录
        os.makedirs(args.path, exist_ok=True)
        os.chdir(args.path)
        
        # 创建目录结构
        os.makedirs('source/_posts', exist_ok=True)
        os.makedirs('source/assets', exist_ok=True)
        
        # 创建自定义主题目录结构
        os.makedirs('source/_templates/themes/custom', exist_ok=True)
        os.makedirs('source/_templates/themes/custom/css', exist_ok=True)
        
        # 创建主题说明文件
        with open('source/_templates/themes/README.md', 'w', encoding='utf-8') as f:
            f.write("""# 自定义主题目录

这个目录用于存放自定义主题。

## 如何使用自定义主题

1. 在 `themes` 目录下创建一个新的文件夹，作为您的主题名称，例如 `mytheme`
2. 在主题文件夹中创建以下文件：
   - `index.html` - 首页模板
   - `post.html` - 文章页模板
   - `tags.html` - 标签列表页模板
   - `tag.html` - 单个标签页模板
   - `rss.xml` - RSS订阅模板
   - `css/style.css` - 样式文件

3. 在 `config.yml` 中设置主题：
   ```yaml
   # 主题设置
   theme: 'mytheme'
   ```

您可以参考 `custom` 目录中的示例文件，或者查看内置主题的源代码作为参考。
内置主题位于 Python 安装目录下的：
```
site-packages/cato/templates/themes/
```

可用的内置主题有：default, pink, sticky
""")
        
        # 创建自定义主题示例文件
        with open('source/_templates/themes/custom/index.html', 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html lang="{{ config.language }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ config.site_name }}</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{{ config.site_name }}</h1>
            <p>{{ config.site_description }}</p>
        </header>

        <main>
            {% if posts %}
            <ul class="post-list">
                {% for post in posts %}
                <li class="post-item">
                    <h2><a href="{{ post.metadata.url }}">{{ post.metadata.title }}</a></h2>
                    <p>{{ post.metadata.date.strftime(config.date_format) }}</p>
                    <p>{{ post.metadata.content[:200] }}...</p>
                </li>
                {% endfor %}
            </ul>
            {% else %}
            <p>还没有文章，请添加您的第一篇文章！</p>
            {% endif %}
        </main>

        <footer>
            <p>&copy; {{ now().year }} {{ config.site_name }}</p>
        </footer>
    </div>
</body>
</html>""")
        
        with open('source/_templates/themes/custom/css/style.css', 'w', encoding='utf-8') as f:
            f.write("""/* 自定义主题样式 */
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
    color: #333;
}

.container {
    width: 80%;
    margin: auto;
    overflow: hidden;
    padding: 20px;
}

.header {
    background: #333;
    color: #fff;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
}

.post-list {
    list-style: none;
    padding: 0;
}

.post-item {
    background: #fff;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

a {
    color: #333;
    text-decoration: none;
}

a:hover {
    color: #555;
}

footer {
    background: #333;
    color: #fff;
    text-align: center;
    padding: 10px;
    margin-top: 20px;
}""")
        
        # 创建public目录，确保服务器可以启动
        os.makedirs('public', exist_ok=True)
        
        # 复制配置文件
        if not os.path.exists('config.yml'):
            shutil.copy(
                os.path.join(os.path.dirname(__file__), 'config.yml'),
                'config.yml'
            )
        
        # 创建示例文章
        if not os.path.exists('source/_posts/hello-world.md'):
            with open('source/_posts/hello-world.md', 'w', encoding='utf-8') as f:
                f.write("""---
title: 你好，世界
date: 2023-01-01
tags: [示例, 博客]
author: 博主
draft: false
---

这是我的第一篇博客文章。

## 关于这个博客

这是使用 Cato 静态博客生成器创建的网站。

## 功能特点

1. 支持 Markdown 写作
2. 自动生成标签页面
3. 响应式设计
4. RSS 订阅支持

## 代码示例

```python
print("Hello, World!")
```

祝您使用愉快！
""")
        
        # 创建 .gitignore 文件
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write("""# 忽略所有文件和目录
/*

# 不忽略 public 目录中的内容
!/*.html
!/css/
!/posts/
!/tags/
!feed.xml

# 忽略系统文件
.DS_Store
Thumbs.db

# 忽略 Python 缓存文件
__pycache__/
*.py[cod]
""")

        # 初始化 Git 仓库
        os.system('git init')
        
        print("✨ 博客初始化完成！")
        print("\n下一步：")
        print("1. 编辑 config.yml 配置文件")
        print("2. 运行 'cato serve' 或 'cato s' 启动开发服务器")
        print("3. 自定义主题位于 source/_templates/themes/ 目录")
        print("\nGitHub Pages 部署说明：")
        print("1. 在 GitHub 创建仓库：用户名.github.io")
        print("2. 添加远程仓库：git remote add origin https://github.com/用户名/用户名.github.io.git")
        print("3. 构建并部署：cato d")
        print("\n注意：只有 public 目录中构建后的文件会被推送到 GitHub")
        
    except Exception as e:
        print(f"错误: 初始化博客失败 - {e}")
        sys.exit(1)

def new_post(args):
    """创建新文章"""
    if not args.title:
        print("错误: 请提供文章标题")
        sys.exit(1)
        
    try:
        # 生成文件名
        date = args.date or datetime.now().strftime('%Y-%m-%d')
        title_slug = args.title.lower().replace(' ', '-')
        filename = f"{date}-{title_slug}.md"
        filepath = os.path.join('source/_posts', filename)
        
        # 创建文章
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"""---
title: {args.title}
date: {date}
tags: []
author: {args.author or '博主'}
draft: {str(args.draft).lower()}
---

""")
        
        print(f"✨ 文章创建成功：{filepath}")
        
    except Exception as e:
        print(f"错误: 创建文章失败 - {e}")
        sys.exit(1)

def serve(args):
    """启动开发服务器"""
    try:
        print("正在初始化博客构建器...")
        builder = BlogBuilder('config.yml')
        
        # 先构建博客
        print("构建博客内容...")
        builder.build(include_drafts=args.drafts)
        
        # 检查是否成功构建了public目录
        if not os.path.exists('public'):
            print("错误: 未能成功构建博客内容，public目录不存在")
            print("尝试手动创建public目录...")
            os.makedirs('public', exist_ok=True)
            
        # 检查是否有index.html
        if not os.path.exists('public/index.html'):
            print("警告: 未找到首页文件，可能无法正常访问博客")
            print("创建临时首页...")
            with open('public/index.html', 'w', encoding='utf-8') as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>博客正在构建中</title>
</head>
<body>
    <h1>博客正在构建中</h1>
    <p>如果您看到此页面，说明博客正在初始化。请检查您的配置和文章。</p>
    <p>您可以访问 <a href="/admin">管理后台</a> 添加文章。</p>
</body>
</html>""")
        
        try:
            print(f"尝试在端口 {args.port} 启动服务器...")
            server = BlogDevServer(port=args.port)
            server.run(builder)
        except OSError as e:
            if "Address already in use" in str(e) or "10048" in str(e):  # 端口被占用
                print(f"错误: 端口 {args.port} 已被占用，尝试使用其他端口")
                # 尝试其他端口
                for port in range(args.port + 1, args.port + 10):
                    try:
                        print(f"尝试端口 {port}...")
                        server = BlogDevServer(port=port)
                        server.run(builder)
                        break
                    except OSError:
                        continue
                else:
                    print("无法找到可用端口，请手动指定一个可用端口")
                    print("例如: cato serve --port 8888")
                    sys.exit(1)
            else:
                print(f"启动服务器时出错: {e}")
                raise
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"错误: 启动服务器失败 - {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def build(args):
    """构建静态文件"""
    try:
        builder = BlogBuilder('config.yml')
        builder.build(include_drafts=args.drafts)
        print("✨ 构建完成！")
    except Exception as e:
        print(f"错误: 构建失败 - {e}")
        sys.exit(1)

def clean(args):
    """清理生成的文件"""
    try:
        if os.path.exists('public'):
            shutil.rmtree('public')
            print("✨ 清理完成！")
    except Exception as e:
        print(f"错误: 清理失败 - {e}")
        sys.exit(1)

def deploy(args):
    """部署博客到 GitHub Pages"""
    try:
        # 构建博客
        print("开始构建博客...")
        builder = BlogBuilder('config.yml')
        builder.build()

        # 删除旧的构建文件
        print("清理旧文件...")
        for item in ['css', 'posts', 'tags', 'index.html', 'feed.xml']:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)

        # 复制新构建的文件
        print("复制新文件...")
        for item in os.listdir('public'):
            src = os.path.join('public', item)
            if os.path.isdir(src):
                shutil.copytree(src, item, dirs_exist_ok=True)
            else:
                shutil.copy2(src, item)

        # 提交更改
        print("提交更改...")
        os.system('git add .')
        os.system(f'git commit -m "Update blog content {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"')

        # 推送到远程仓库
        print("推送到 GitHub...")
        os.system('git push origin master')

        print("✨ 部署完成！")

    except Exception as e:
        print(f"错误: 部署失败 - {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Cato 静态博客生成器')
    parser.add_argument('--version', action='version', version=f'Cato {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # init 命令
    init_parser = subparsers.add_parser('init', aliases=['i'], help='初始化新博客 (i: init)')
    init_parser.add_argument('path', help='博客目录路径')
    
    # new 命令
    new_parser = subparsers.add_parser('new', aliases=['n'], help='创建新文章 (n: new)')
    new_parser.add_argument('title', help='文章标题')
    new_parser.add_argument('--date', help='发布日期 (YYYY-MM-DD)')
    new_parser.add_argument('--author', help='作者名')
    new_parser.add_argument('--draft', action='store_true', help='创建为草稿')
    
    # serve 命令
    serve_parser = subparsers.add_parser('serve', aliases=['s'], help='启动开发服务器 (s: server)')
    serve_parser.add_argument('--port', type=int, default=8000, help='服务器端口')
    serve_parser.add_argument('--watch', '-w', action='store_true', help='监视文件变化')
    serve_parser.add_argument('--drafts', '-d', action='store_true', help='包含草稿文章')
    
    # build 命令
    build_parser = subparsers.add_parser('build', aliases=['g'], help='构建静态文件 (g: generate)')
    build_parser.add_argument('--drafts', '-d', action='store_true', help='包含草稿文章')
    
    # clean 命令
    clean_parser = subparsers.add_parser('clean', aliases=['c'], help='清理生成的文件 (c: clean)')
    
    # deploy 命令
    deploy_parser = subparsers.add_parser('deploy', aliases=['d'], help='部署到服务器 (d: deploy)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 执行对应的命令
    commands = {
        'init': init_blog,
        'i': init_blog,    # 别名: init
        'new': new_post,
        'n': new_post,     # 别名: new
        'serve': serve,
        's': serve,        # 别名: server
        'build': build,
        'g': build,        # 别名: generate
        'clean': clean,
        'c': clean,        # 别名: clean
        'deploy': deploy,
        'd': deploy        # 别名: deploy
    }
    
    commands[args.command](args)

if __name__ == '__main__':
    main()

