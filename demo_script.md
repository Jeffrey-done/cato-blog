# Cato 博客系统演示视频脚本

## 开场白 (10秒)

"大家好！今天我要向大家介绍 Cato，一个简单而强大的静态博客生成器。Cato 受到 Hexo 的启发，但更加轻量级和易于使用。让我们一起来看看它的功能。"

## 安装过程 (30秒)

"Cato 的安装非常简单。我们可以使用一行命令完成安装："

```powershell
irm https://raw.githubusercontent.com/Jeffrey-done/cato-blog/master/install_cato_minimal.ps1 | iex
```

"看，安装已经完成了！现在我们可以开始创建我们的第一个博客。"

## 创建新博客 (20秒)

"让我们使用 `cato init` 命令创建一个新博客："

```bash
cato init myblog
cd myblog
```

"Cato 已经为我们创建了一个完整的博客结构，包括配置文件、主题和示例文章。"

## 查看目录结构 (15秒)

"让我们看一下博客的目录结构："

```bash
dir
```

"我们可以看到 `config.yml` 配置文件、`source` 目录和其他必要的文件。"

## 创建新文章 (30秒)

"现在，让我们创建一篇新文章："

```bash
cato new "我的第一篇Cato博客文章"
# 或使用简化命令
cato n "我的第一篇Cato博客文章"
```

"Cato 已经在 `source/_posts` 目录下创建了一个新的 Markdown 文件。让我们编辑这个文件，添加一些内容。"

(打开文件编辑器，添加一些示例内容)

## 构建博客 (20秒)

"现在，让我们构建博客："

```bash
cato build
# 或使用简化命令
cato g
```

"Cato 已经生成了静态 HTML 文件，并将它们放在 `public` 目录中。"

## 启动本地服务器 (30秒)

"让我们启动本地服务器来预览我们的博客："

```bash
cato serve
# 或使用简化命令
cato s
```

"现在，我们可以在浏览器中访问 `http://localhost:8000` 来查看我们的博客。"

(展示浏览器中的博客)

## 切换主题 (40秒)

"Cato 提供了多种内置主题。让我们尝试切换到 'pink' 主题："

(编辑 `config.yml` 文件，将 `theme` 从 'default' 改为 'pink')

```yaml
# 主题设置
theme: 'pink'
```

"现在，让我们重新构建博客并刷新页面："

```bash
cato g
```

(刷新浏览器，展示新主题)

"看，主题已经切换到粉色了！同样，我们还可以尝试 'sticky' 主题，它看起来像便签。"

## 自定义主题 (30秒)

"如果您想创建自己的主题，只需将 `theme` 设置为 'custom'，然后修改 `source/_templates/themes/custom` 目录下的文件。"

(展示自定义主题目录)

"您可以根据自己的需求修改 HTML、CSS 和 JavaScript 文件。"

## 结束语 (15秒)

"这就是 Cato 博客系统的基本功能演示。它简单、高效，非常适合那些想要快速搭建个人博客的用户。感谢观看，如果您有任何问题，请在评论区留言。" 