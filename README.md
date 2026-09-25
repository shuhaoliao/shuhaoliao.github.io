# Shuhao Liao — Academic Homepage

A responsive, single-page research website for **https://shuhaoliao.github.io**.
The introduction, news, and all seven selected publications live on the same page. The top navigation scrolls to each section.

## 本地预览

在仓库目录运行：

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

打开 http://127.0.0.1:8765/ 。也可以直接打开 `index.html`；通过本地服务器预览可使用剪贴板功能。

## 编辑内容

1. 修改 `content/site.json` 中的简介、个人链接、动态和论文。
2. 在仓库根目录运行 `python scripts/build_site.py`。
3. 刷新浏览器检查效果，将修改后的源文件及生成文件一起提交。

`position`、`affiliations`、`email`、`scholar` 和简介中的导师信息已按本人提供的资料填写。`cv` 尚未填写，补充后重新生成即可显示。Email、Google Scholar、GitHub 按顺序显示在照片下方。`bio` 的每段可以是普通字符串，也可以是由 `text` 和可选 `url` 组成的片段数组，用于在简介中添加导师链接。论文来源和资料依据记录在 `content/SOURCES.md`。

- `index.html`：生成后的完整静态页面；不依赖 JavaScript 即可阅读正文和论文。
- `assets/site/style.css`：排版、移动端适配、深色模式和打印样式。
- `assets/site/main.js`：主题切换、按需加载的动态预览、BibTeX 复制。
- `assets/site/media/`：头像、论文预览及压缩后的视频。
- `scripts/build_site.py`：仅使用 Python 标准库的生成脚本。
- `publications.bib`：全部展示论文的 BibTeX。

## GitHub Pages 部署

网站是普通 HTML/CSS/JavaScript，**无需 npm、Ruby 或 Jekyll 构建**。`.nojekyll` 让 GitHub Pages 直接发布静态文件。

在 GitHub 仓库 **Settings → Pages** 中使用 **Deploy from a branch**，选择 `master` 分支、`/(root)` 目录。提交并推送本地修改后，GitHub Pages 会更新网站。

本次制作仅修改本地文件，没有自动提交或推送。原仓库的 AcademicPages 模板文件保留用于追溯，不参与新版首页渲染。`/about/`、`/news/`、`/publications/` 是旧链接兼容入口，只会跳转到首页对应位置。

## 设计与素材

页面参考 https://jingsongliang.com/ 的学术主页信息结构，独立实现单页布局与样式。头像和论文展示素材由站点作者提供。没有外部字体、CDN、访客追踪或第三方脚本依赖。

原 AcademicPages 模板的 MIT 许可见 `LICENSE`。
