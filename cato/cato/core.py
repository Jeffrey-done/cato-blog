import os
import shutil
import markdown
import frontmatter
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import time
from pathlib import Path
import argparse
import yaml
import http.server
import socketserver
import webbrowser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import base64
import hashlib
import secrets
import urllib.parse

# 配置路径
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = Path('source')  # 使用 source 目录
OUTPUT_DIR = Path('public')  # 输出目录
POSTS_DIR = SRC_DIR / '_posts'
TEMPLATES_DIR = BASE_DIR / 'templates'  # 使用包内模板
ASSETS_DIR = SRC_DIR / 'assets'

class BlogConfig:
    def __init__(self, config_file=None):
        self.config = {
            'site_name': '我的博客',
            'site_description': '分享技术与生活',
            'site_url': 'http://localhost:8000',
            'author': '博主',
            'language': 'zh-CN',
            'theme': 'default',  # 默认主题
            'posts_per_page': 10,
            'date_format': '%Y-%m-%d',
            'markdown_extensions': [
                'fenced_code',
                'codehilite',
                'tables',
                'toc',
                'footnotes'
            ]
        }
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    self.config.update(user_config)

    def __getitem__(self, key):
        return self.config.get(key)

class BlogBuilder:
    def __init__(self, config_file=None):
        self.config = BlogConfig(config_file)
        
        # 设置模板搜索路径
        # 首先检查本地自定义主题
        local_theme_dir = Path('source') / '_templates' / 'themes' / self.config['theme']
        theme_dir = TEMPLATES_DIR / 'themes' / self.config['theme']
        
        # 设置模板搜索路径，优先使用本地自定义主题
        template_dirs = []
        
        # 如果本地存在自定义主题，优先使用
        if local_theme_dir.exists():
            print(f"使用本地自定义主题: {self.config['theme']}")
            template_dirs.append(local_theme_dir)
            
            # 添加本地基础模板目录
            local_templates_dir = Path('source') / '_templates'
            if local_templates_dir.exists():
                template_dirs.append(local_templates_dir)
        else:
            # 使用内置主题
            if theme_dir.exists():
                template_dirs.append(theme_dir)
            else:
                print(f"警告: 未找到主题 '{self.config['theme']}'，使用默认主题")
                self.config.config['theme'] = 'default'
                template_dirs.append(TEMPLATES_DIR / 'themes' / 'default')
        
        # 添加内置基础模板和管理后台模板
        template_dirs.append(TEMPLATES_DIR)
        template_dirs.append(TEMPLATES_DIR / 'admin')
        
        self.env = Environment(loader=FileSystemLoader(template_dirs))
        
        # 添加全局函数
        self.env.globals['now'] = datetime.now
        
        self.posts = []
        self.tags = {}
        self.drafts = []

    def clean_output(self):
        """清理输出目录"""
        if OUTPUT_DIR.exists():
            try:
                shutil.rmtree(OUTPUT_DIR)
            except Exception as e:
                print(f"清理输出目录失败: {e}")
                print("等待5秒后重试...")
                time.sleep(5)
                try:
                    shutil.rmtree(OUTPUT_DIR)
                except Exception as e:
                    print(f"第二次尝试失败: {e}")
                    print("创建新的输出目录...")
        
        try:
            OUTPUT_DIR.mkdir(parents=True)
            (OUTPUT_DIR / 'posts').mkdir()
            (OUTPUT_DIR / 'tags').mkdir()
            (OUTPUT_DIR / 'assets').mkdir()
        except Exception as e:
            print(f"创建目录失败: {e}")
            raise

    def load_posts(self, include_drafts=False):
        """加载所有文章"""
        # 确保文章目录存在
        if not POSTS_DIR.exists():
            print(f"文章目录不存在: {POSTS_DIR}")
            print("创建文章目录...")
            os.makedirs(POSTS_DIR, exist_ok=True)
            return

        for file in POSTS_DIR.glob('*.md'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    
                    # 处理草稿
                    is_draft = post.metadata.get('draft', False)
                    if is_draft and not include_drafts:
                        self.drafts.append(post)
                        continue

                    # 解析文件名中的日期
                    date_str = file.stem[:10]
                    try:
                        post.metadata['date'] = datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        print(f"警告: 文件名日期格式错误: {file.name}")
                        post.metadata['date'] = datetime.now()

                    # 设置URL和文件名
                    post.metadata['url'] = f'/posts/{file.stem}.html'
                    post.metadata['filename'] = file.stem
                    
                    # 处理标签
                    if 'tags' in post.metadata:
                        for tag in post.metadata['tags']:
                            if tag not in self.tags:
                                self.tags[tag] = []
                            self.tags[tag].append(post)
                    
                    # 转换Markdown为HTML
                    html_content = markdown.markdown(
                        post.content,
                        extensions=self.config['markdown_extensions']
                    )
                    post.metadata['content'] = html_content
                    
                    # 添加作者信息
                    if 'author' not in post.metadata:
                        post.metadata['author'] = self.config['author']
                    
                    self.posts.append(post)
            except Exception as e:
                print(f"处理文章失败 {file.name}: {e}")
        
        # 按日期排序
        self.posts.sort(key=lambda x: x.metadata['date'], reverse=True)

    def copy_assets(self):
        """复制静态资源"""
        if ASSETS_DIR.exists():
            try:
                if (OUTPUT_DIR / 'assets').exists():
                    shutil.rmtree(OUTPUT_DIR / 'assets')
                shutil.copytree(ASSETS_DIR, OUTPUT_DIR / 'assets')
            except Exception as e:
                print(f"复制资源文件失败: {e}")

    def build_posts(self):
        """生成文章页面"""
        template = self.env.get_template('post.html')
        for post in self.posts:
            output_path = OUTPUT_DIR / 'posts' / f"{post.metadata['filename']}.html"
            try:
                html = template.render(post=post, config=self.config)
                output_path.write_text(html, encoding='utf-8')
            except Exception as e:
                print(f"生成文章页面失败 {output_path.name}: {e}")

    def build_index(self):
        """生成首页"""
        template = self.env.get_template('index.html')
        try:
            # 分页
            posts_per_page = self.config['posts_per_page']
            total_pages = max(1, (len(self.posts) + posts_per_page - 1) // posts_per_page)
            
            for page in range(total_pages):
                start = page * posts_per_page
                end = start + posts_per_page
                current_posts = self.posts[start:end]
                
                context = {
                    'posts': current_posts,
                    'config': self.config,
                    'pagination': {
                        'current': page + 1,
                        'total': total_pages,
                        'has_prev': page > 0,
                        'has_next': page < total_pages - 1,
                        'prev_url': f'/page/{page}.html' if page > 0 else None,
                        'next_url': f'/page/{page + 2}.html' if page < total_pages - 1 else None
                    } if self.posts else None
                }
                
                if page == 0:
                    output_path = OUTPUT_DIR / 'index.html'
                else:
                    (OUTPUT_DIR / 'page').mkdir(exist_ok=True)
                    output_path = OUTPUT_DIR / 'page' / f'{page + 1}.html'
                
                html = template.render(**context)
                output_path.write_text(html, encoding='utf-8')
        except Exception as e:
            print(f"生成首页失败: {e}")

    def build_tags(self):
        """生成标签相关页面"""
        # 生成标签列表页
        try:
            template = self.env.get_template('tags.html')
            html = template.render(tags=self.tags, config=self.config)
            (OUTPUT_DIR / 'tags.html').write_text(html, encoding='utf-8')
        except Exception as e:
            print(f"生成标签列表页失败: {e}")

        # 生成各标签的文章列表页
        template = self.env.get_template('tag.html')
        for tag, posts in self.tags.items():
            try:
                output_path = OUTPUT_DIR / 'tags' / f"{tag}.html"
                html = template.render(tag=tag, posts=posts, config=self.config)
                output_path.write_text(html, encoding='utf-8')
            except Exception as e:
                print(f"生成标签页面失败 {tag}: {e}")

    def build_rss(self):
        """生成RSS订阅"""
        try:
            template = self.env.get_template('rss.xml')
            html = template.render(
                posts=self.posts[:10],
                config=self.config,
                build_date=datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            )
            (OUTPUT_DIR / 'feed.xml').write_text(html, encoding='utf-8')
        except Exception as e:
            print(f"生成RSS失败: {e}")

    def build(self, include_drafts=False):
        """执行完整的构建流程"""
        print("开始构建博客...")
        start_time = time.time()
        
        try:
            print("1. 清理输出目录...")
            self.clean_output()
            
            print("2. 加载文章...")
            self.load_posts(include_drafts)
            print(f"   找到 {len(self.posts)} 篇文章")
            if include_drafts:
                print(f"   找到 {len(self.drafts)} 篇草稿")
            print(f"   找到 {len(self.tags)} 个标签")
            
            print("3. 复制静态资源...")
            self.copy_assets()
            
            # 创建CSS目录
            os.makedirs(os.path.join(OUTPUT_DIR, 'css'), exist_ok=True)
            
            # 首先检查本地自定义主题的CSS文件
            local_theme_css_dir = os.path.join('source', '_templates', 'themes', self.config['theme'], 'css')
            if os.path.exists(local_theme_css_dir):
                print("   复制本地主题CSS文件...")
                for css_file in os.listdir(local_theme_css_dir):
                    if css_file.endswith('.css'):
                        shutil.copy2(
                            os.path.join(local_theme_css_dir, css_file),
                            os.path.join(OUTPUT_DIR, 'css', css_file)
                        )
            else:
                # 如果本地没有，使用内置主题的CSS文件
                theme_css_dir = os.path.join(os.path.dirname(__file__), 'templates', 'themes', self.config['theme'], 'css')
                if os.path.exists(theme_css_dir):
                    print("   复制主题CSS文件...")
                    for css_file in os.listdir(theme_css_dir):
                        if css_file.endswith('.css'):
                            shutil.copy2(
                                os.path.join(theme_css_dir, css_file),
                                os.path.join(OUTPUT_DIR, 'css', css_file)
                            )
            
            try:
                print("4. 生成文章页面...")
                self.build_posts()
            except Exception as e:
                print(f"生成文章页面失败: {e}")
            
            try:
                print("5. 生成首页...")
                self.build_index()
            except Exception as e:
                print(f"生成首页失败: {e}")
                # 创建一个简单的首页
                index_path = os.path.join(OUTPUT_DIR, 'index.html')
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.config['site_name']}</title>
</head>
<body>
    <h1>博客正在构建中</h1>
    <p>如果您看到此页面，说明博客正在初始化。请检查您的配置和文章。</p>
    <p>您可以访问 <a href="/admin">管理后台</a> 添加文章。</p>
</body>
</html>""")
                print("警告: 未找到首页文件，可能无法正常访问博客")
                print("创建临时首页...")
            
            try:
                print("6. 生成标签页面...")
                self.build_tags()
            except Exception as e:
                print(f"生成标签页面失败: {e}")
            
            try:
                print("7. 生成RSS订阅...")
                self.build_rss()
            except Exception as e:
                print(f"生成RSS失败: {e}")
            
            end_time = time.time()
            print(f"\n博客构建完成！用时 {end_time - start_time:.2f} 秒")
            
        except Exception as e:
            print(f"\n构建过程中出错: {e}")
            import traceback
            traceback.print_exc()
            # 创建基本的输出目录，确保服务器可以启动
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            # 创建一个简单的首页
            index_path = os.path.join(OUTPUT_DIR, 'index.html')
            with open(index_path, 'w', encoding='utf-8') as f:
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

class AdminHandler:
    def __init__(self, builder):
        self.builder = builder
        self.sessions = {}
        self.admin_password = os.environ.get('BLOG_ADMIN_PASSWORD', 'admin123')
        self.session_timeout = 3600  # 1小时会话超时
        
    def handle_request(self, handler):
        if handler.path.startswith('/admin'):
            # 检查会话
            cookie = handler.headers.get('Cookie', '')
            session_id = None
            for c in cookie.split(';'):
                if c.strip().startswith('session_id='):
                    session_id = c.strip().split('=')[1]
                    break
            
            if not session_id or session_id not in self.sessions:
                if handler.path == '/admin/login' and handler.command == 'POST':
                    return self.handle_login(handler)
                else:
                    return self.serve_login_page(handler)
            
            # 处理管理请求
            if handler.path == '/admin':
                return self.serve_admin_page(handler)
            elif handler.path == '/admin/posts':
                return self.handle_posts(handler)
            elif handler.path == '/admin/post/new':
                return self.handle_new_post(handler)
            elif handler.path.startswith('/admin/post/edit/'):
                return self.handle_edit_post(handler)
            elif handler.path.startswith('/admin/post/delete/'):
                return self.handle_delete_post(handler)
            else:
                handler.send_error(404)
        return False
        
    def serve_login_page(self, handler):
        template = self.builder.env.get_template('admin/login.html')
        content = template.render(config=self.builder.config)
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(content.encode())
        return True
        
    def handle_login(self, handler):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length).decode()
        params = urllib.parse.parse_qs(post_data)
        
        password = params.get('password', [''])[0]
        if password == self.admin_password:
            session_id = secrets.token_urlsafe(32)
            self.sessions[session_id] = {
                'created_at': time.time()
            }
            handler.send_response(302)
            handler.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly')
            handler.send_header('Location', '/admin')
            handler.end_headers()
        else:
            template = self.builder.env.get_template('admin/login.html')
            content = template.render(config=self.builder.config, error='密码错误')
            handler.send_response(200)
            handler.send_header('Content-type', 'text/html')
            handler.end_headers()
            handler.wfile.write(content.encode())
        return True

    def serve_admin_page(self, handler):
        template = self.builder.env.get_template('admin/index.html')
        content = template.render(
            config=self.builder.config,
            posts=self.builder.posts,
            drafts=self.builder.drafts
        )
        handler.send_response(200)
        handler.send_header('Content-type', 'text/html')
        handler.end_headers()
        handler.wfile.write(content.encode())
        return True

    def handle_posts(self, handler):
        if handler.command == 'GET':
            template = self.builder.env.get_template('admin/posts.html')
            content = template.render(
                config=self.builder.config,
                posts=self.builder.posts
            )
            handler.send_response(200)
            handler.send_header('Content-type', 'text/html')
            handler.end_headers()
            handler.wfile.write(content.encode())
        return True

    def handle_new_post(self, handler):
        if handler.command == 'GET':
            template = self.builder.env.get_template('admin/edit.html')
            content = template.render(
                config=self.builder.config,
                post=None,
                is_new=True
            )
            handler.send_response(200)
            handler.send_header('Content-type', 'text/html')
            handler.end_headers()
            handler.wfile.write(content.encode())
        elif handler.command == 'POST':
            content_length = int(handler.headers['Content-Length'])
            post_data = handler.rfile.read(content_length).decode()
            params = urllib.parse.parse_qs(post_data)
            
            title = params.get('title', [''])[0]
            content = params.get('content', [''])[0]
            tags = params.get('tags', [''])[0].split(',')
            is_draft = 'is_draft' in params
            
            # 创建新文章
            date = datetime.now()
            filename = f"{date.strftime('%Y-%m-%d')}-{self._slugify(title)}.md"
            
            post_content = f"""---
title: {title}
date: {date.strftime('%Y-%m-%d %H:%M:%S')}
tags: {tags}
draft: {str(is_draft).lower()}
---

{content}"""
            
            with open(POSTS_DIR / filename, 'w', encoding='utf-8') as f:
                f.write(post_content)
            
            # 重新构建
            self.builder.build()
            
            handler.send_response(302)
            handler.send_header('Location', '/admin')
            handler.end_headers()
        return True

    def handle_edit_post(self, handler):
        filename = handler.path.split('/')[-1]
        post_path = POSTS_DIR / f"{filename}.md"
        
        if handler.command == 'GET':
            if not post_path.exists():
                handler.send_error(404)
                return True
                
            with open(post_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            template = self.builder.env.get_template('admin/edit.html')
            content = template.render(
                config=self.builder.config,
                post=post,
                is_new=False
            )
            handler.send_response(200)
            handler.send_header('Content-type', 'text/html')
            handler.end_headers()
            handler.wfile.write(content.encode())
        elif handler.command == 'POST':
            content_length = int(handler.headers['Content-Length'])
            post_data = handler.rfile.read(content_length).decode()
            params = urllib.parse.parse_qs(post_data)
            
            title = params.get('title', [''])[0]
            content = params.get('content', [''])[0]
            tags = params.get('tags', [''])[0].split(',')
            is_draft = 'is_draft' in params
            
            with open(post_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            post.metadata['title'] = title
            post.metadata['tags'] = tags
            post.metadata['draft'] = is_draft
            post.content = content
            
            with open(post_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            # 重新构建
            self.builder.build()
            
            handler.send_response(302)
            handler.send_header('Location', '/admin')
            handler.end_headers()
        return True

    def handle_delete_post(self, handler):
        """删除文章处理函数"""
        if handler.command != 'POST':
            handler.send_error(405, "Method Not Allowed")
            return True

        # 获取请求体中的数据
        content_length = int(handler.headers.get('Content-Length', 0))
        if content_length > 0:
            post_data = handler.rfile.read(content_length).decode()
            try:
                data = json.loads(post_data)
                filename = data.get('filename', '')
            except:
                filename = ''
        else:
            filename = handler.path.split('/')[-1]
        
        # 安全检查
        if not filename or '..' in filename or '/' in filename:
            handler.send_error(400, "Invalid filename")
            return True

        # 重置文章列表
        self.builder.posts = []
        self.builder.tags = {}
        self.builder.drafts = []
        
        # 使用相对路径
        post_path = POSTS_DIR / f"{filename}.md"
        print(f"尝试删除文件: {post_path} (当前目录: {os.getcwd()})")
        
        try:
            if not post_path.exists():
                print(f"文件不存在: {post_path}")
                handler.send_error(404, "File not found")
                return True
                
            if not post_path.is_file():
                print(f"不是文件: {post_path}")
                handler.send_error(400, "Not a file")
                return True
                
            print(f"删除文件: {post_path}")
            post_path.unlink()  # 使用 Path.unlink() 代替 os.remove()
            
            print("重新构建博客...")
            # 重新构建
            self.builder.build()
            
            # 返回成功响应
            handler.send_response(200)
            handler.send_header('Content-Type', 'application/json')
            handler.end_headers()
            handler.wfile.write(json.dumps({
                'success': True,
                'message': '文章删除成功'
            }).encode())
        except Exception as e:
            print(f"删除文件失败: {e}")
            handler.send_response(500)
            handler.send_header('Content-Type', 'application/json')
            handler.end_headers()
            handler.wfile.write(json.dumps({
                'success': False,
                'message': f'删除文章失败: {str(e)}'
            }).encode())
        
        return True

    def _slugify(self, text):
        """将标题转换为URL友好的格式"""
        text = text.lower()
        text = ''.join(c for c in text if c.isalnum() or c == ' ')
        text = text.replace(' ', '-')
        return text

class BlogDevServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.builder = None
        self.admin = None
        
    def run(self, builder):
        self.builder = builder
        self.admin = AdminHandler(builder)
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self2, *args, **kwargs):
                super().__init__(*args, directory=str(OUTPUT_DIR), **kwargs)
            
            def do_GET(self2):
                if self.admin.handle_request(self2):
                    return
                    
                if self2.path == '/':
                    self2.path = '/index.html'
                elif self2.path.endswith('/'):
                    self2.path += 'index.html'
                return super().do_GET()
                
            def do_POST(self2):
                if self.admin.handle_request(self2):
                    return
                self2.send_error(405)

        # 设置允许服务器立即重用地址
        socketserver.TCPServer.allow_reuse_address = True
        
        with socketserver.TCPServer((self.host, self.port), Handler) as httpd:
            print(f"开发服务器运行在 http://{self.host}:{self.port}")
            print(f"后台管理地址: http://{self.host}:{self.port}/admin")
            print(f"按 Ctrl+C 可以停止服务器")
            webbrowser.open(f"http://{self.host}:{self.port}")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n正在关闭服务器...")
                httpd.server_close()
                print("服务器已停止")

class BlogWatcher(FileSystemEventHandler):
    def __init__(self, builder):
        self.builder = builder
        self.last_build = 0
        self.build_delay = 2  # 延迟2秒再构建

    def on_any_event(self, event):
        if event.is_directory:
            return
            
        current_time = time.time()
        if current_time - self.last_build > self.build_delay:
            print(f"\n检测到文件变化: {event.src_path}")
            self.builder.build(include_drafts=True)
            self.last_build = current_time

def main():
    parser = argparse.ArgumentParser(description='静态博客生成器')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--serve', '-s', action='store_true', help='启动开发服务器')
    parser.add_argument('--watch', '-w', action='store_true', help='监视文件变化')
    parser.add_argument('--drafts', '-d', action='store_true', help='包含草稿文章')
    parser.add_argument('--port', '-p', type=int, default=8000, help='开发服务器端口')
    
    args = parser.parse_args()
    
    # 创建构建器
    builder = BlogBuilder(args.config)
    
    # 构建站点
    builder.build(include_drafts=args.drafts)
    
    # 如果需要启动服务器
    if args.serve:
        if args.watch:
            # 启动文件监视
            observer = Observer()
            observer.schedule(BlogWatcher(builder), str(SRC_DIR), recursive=True)
            observer.start()
            
        # 启动开发服务器
        server = BlogDevServer(port=args.port)
        try:
            server.run(builder)
        except KeyboardInterrupt:
            if args.watch:
                observer.stop()
                observer.join()
            print("\n服务器已停止")

if __name__ == '__main__':
    main() 