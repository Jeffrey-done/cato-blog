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
date: 2024-03-15
tags: [示例, 博客]
author: 博主
---

这是我的第一篇博客文章。

## 关于这个博客

这是使用 Cato 创建的静态博客网站。

## 功能特点

1. 支持 Markdown 写作
2. 自动生成标签页面
3. 响应式设计
4. RSS 订阅支持

## 代码示例

```python
print("Hello, World!")
```

祝您使用愉快！""")
        
        print("✨ 博客初始化完成！")
        print("\n下一步：")
        print("1. 编辑 config.yml 配置文件")
        print("2. 运行 'cato serve' 启动开发服务器")
        
    except Exception as e:
        print(f"错误: 初始化失败 - {e}")
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
        builder = BlogBuilder('config.yml')
        try:
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
                raise
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"错误: 启动服务器失败 - {e}")
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
    """部署到服务器"""
    try:
        # 先构建
        builder = BlogBuilder('config.yml')
        builder.build()
        
        # 读取部署配置
        if not os.path.exists('deploy.yml'):
            print("错误: 未找到部署配置文件 deploy.yml")
            sys.exit(1)
            
        # TODO: 实现部署逻辑
        print("部署功能开发中...")
        
    except Exception as e:
        print(f"错误: 部署失败 - {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Cato 静态博客生成器')
    parser.add_argument('--version', action='version', version=f'Cato {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化新博客')
    init_parser.add_argument('path', help='博客目录路径')
    
    # new 命令
    new_parser = subparsers.add_parser('new', help='创建新文章')
    new_parser.add_argument('title', help='文章标题')
    new_parser.add_argument('--date', help='发布日期 (YYYY-MM-DD)')
    new_parser.add_argument('--author', help='作者名')
    new_parser.add_argument('--draft', action='store_true', help='创建为草稿')
    
    # serve 命令
    serve_parser = subparsers.add_parser('serve', help='启动开发服务器')
    serve_parser.add_argument('--port', type=int, default=8000, help='服务器端口')
    serve_parser.add_argument('--watch', '-w', action='store_true', help='监视文件变化')
    
    # build 命令
    build_parser = subparsers.add_parser('build', help='构建静态文件')
    build_parser.add_argument('--drafts', '-d', action='store_true', help='包含草稿文章')
    
    # clean 命令
    clean_parser = subparsers.add_parser('clean', help='清理生成的文件')
    
    # deploy 命令
    deploy_parser = subparsers.add_parser('deploy', help='部署到服务器')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 执行对应的命令
    commands = {
        'init': init_blog,
        'new': new_post,
        'serve': serve,
        'build': build,
        'clean': clean,
        'deploy': deploy
    }
    
    commands[args.command](args)

if __name__ == '__main__':
    main()

