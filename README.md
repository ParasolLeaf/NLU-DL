# NLU-DL 课程网站 - 静态版本

基于深度学习的自然语言理解课程网站，纯静态HTML版本，可直接部署到 GitHub Pages。

## 🌟 功能特性

- 📚 课程信息完整展示
- 📖 教学团队介绍
- 📝 课程内容概览
- 🎯 响应式设计
- 📱 响应式设计
- 🎨 现代化UI界面
- ⚡ 纯静态，加载速度快

## 🚀 快速部署

### 方法一：直接上传文件
1. 将 `index.html` 文件上传到 GitHub 仓库根目录
2. 在仓库设置中启用 GitHub Pages
3. 选择 "Deploy from a branch" -> "main" -> "/ (root)"

### 方法二：使用 Git
```bash
git add .
git commit -m "Add static course website"
git push origin main
```

### 方法三：Next.js 构建（可选）
如果需要使用 Next.js 版本：

```bash
npm install
npm run dev
npm run export
npm run deploy
```

## 📁 项目结构

```
├── index.html             # 主页面（静态HTML）
├── app/                   # Next.js 版本（可选）
├── components/            # React 组件（可选）
├── package.json           # 项目配置
├── next.config.mjs        # Next.js 配置
└── README.md              # 说明文档
```

## 🛠️ 技术栈

- **主版本**: 纯 HTML + CSS + JavaScript
- **可选框架**: Next.js 14（用于开发）
- **样式**: 原生 CSS（响应式设计）
- **部署**: GitHub Pages
- **兼容性**: 所有现代浏览器

## ✨ 特色功能

1. **纯静态** - 无需服务器，直接在 GitHub Pages 运行
2. **响应式** - 完美适配手机、平板、桌面设备
3. **现代设计** - 采用北京大学品牌色彩和现代UI设计
4. **平滑动画** - 包含悬停效果和滚动动画
5. **SEO友好** - 语义化HTML结构

## 🎨 自定义修改

要修改课程信息，直接编辑 `index.html` 文件中的相应内容：
- 课程标题和描述
- 教师信息
- 课程时间安排
- 联系方式等

网站将在 `https://yourusername.github.io/repository-name/` 访问。