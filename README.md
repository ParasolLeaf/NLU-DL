# NLU-DL 课程网站

基于深度学习的自然语言理解课程网站，使用 Next.js 构建的静态网站，部署在 GitHub Pages 上。

## 🌟 功能特性

- 📚 课程信息展示
- 📖 课程材料浏览
- 📝 作业信息查看
- 🎯 项目要求展示
- 📱 响应式设计
- 🎨 现代化UI界面

## 🚀 部署方式

### GitHub Pages 部署

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "Deploy to GitHub Pages"
   git push origin gh-pages
   ```

2. **配置 GitHub Pages**
   - 进入仓库设置 (Settings)
   - 找到 "Pages" 选项
   - 在 "Source" 中选择 "Deploy from a branch"
   - 选择 "gh-pages" 分支
   - 点击 "Save"

3. **自动部署**
   - 每次推送到 main 分支时，GitHub Actions 会自动构建并部署到 gh-pages 分支
   - 部署完成后，网站将在 `https://yourusername.github.io/NLU-DL-SERVER/` 可用

### 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 手动部署到 gh-pages
npm run deploy
```

## 📁 项目结构

```
├── app/                    # Next.js 应用页面
│   ├── page.tsx           # 主页
│   ├── materials/         # 课程材料页面
│   ├── assignments/       # 作业页面
│   ├── projects/          # 项目页面
│   └── admin/             # 管理页面（静态模式）
├── components/            # React 组件
│   ├── navigation.tsx     # 导航组件
│   └── ui/               # UI 组件库
├── .github/workflows/     # GitHub Actions 配置
└── public/               # 静态资源
```

## 🛠️ 技术栈

- **框架**: Next.js 14
- **样式**: Tailwind CSS
- **UI组件**: Radix UI + shadcn/ui
- **部署**: GitHub Pages
- **CI/CD**: GitHub Actions

## 📝 注意事项

- 此版本为静态网站，不支持文件上传和动态数据管理
- 管理功能在静态模式下不可用
- 所有数据都是预设的静态内容
- 适合用作课程信息展示和学生查看材料

## 🔧 自定义配置

如需修改课程信息、材料或作业内容，请编辑对应页面文件中的静态数据部分。
