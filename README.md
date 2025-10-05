# NLU-DL 课程网站 (gh-pages-src分支开发版本)

基于深度学习的自然语言理解课程网站，使用 Next.js 构建，支持完整的页面跳转和文件下载功能。

**注意：此项目的开发代码位于 gh-pages-src 分支，master 分支保持不变。**

## 🌟 功能特性

- 📚 完整的课程信息管理系统
- 📖 课程材料浏览和下载
- 📝 作业发布和管理
- 🚀 项目展示和要求
- 📱 响应式设计
- 🎨 现代化UI界面
- ⚡ 快速页面跳转
- 📁 文件下载功能

## 🚀 快速部署

### 1. 推送到 GitHub gh-pages-src分支
```bash
git add .
git commit -m "Update course website"
git push origin gh-pages-src  # 推送到gh-pages-src分支
```

### 2. 配置 GitHub Pages
1. 进入 GitHub 仓库设置
2. 找到 "Pages" 选项
3. 在 "Source" 中选择 "Github Action"
4. 保存设置

### 3. 工作流程
- 开发代码保持在 `gh-pages-src` 分支
- 代码推送到 `gh-pages-src` 分支触发构建
- GitHub Actions 自动构建
- 构建后的静态文件覆盖 `gh-pages` 分支
- GitHub Pages 从 `gh-pages` 分支提供服务

### 4. 本地开发
```bash
# 安装依赖
npm install

# 构建生产版本
npm run build

# 启动开发服务器
npm run dev
```

## 📁 项目结构

```
├── app/                   # Next.js 应用页面
│   ├── page.tsx          # 首页
│   ├── materials/        # 课程材料页面
│   ├── assignments/      # 作业页面
│   ├── projects/         # 项目页面
│   └── admin/            # 管理页面
├── components/            # React 组件
├── public/files/         # 课程文件存储
│   ├── materials/        # 课程材料文件
│   ├── assignments/      # 作业文件
│   └── projects/         # 项目范例文件
├── package.json           # 项目配置
├── next.config.mjs        # Next.js 配置
└── README.md              # 说明文档
```

## 🛠️ 技术栈

- **框架**: Next.js 14 + React 18
- **样式**: Tailwind CSS + shadcn/ui
- **图标**: Lucide React
- **部署**: GitHub Pages
- **构建**: 静态导出 (SSG)

## ✨ 功能说明

### 页面功能
- **首页** - 课程概览和基本信息
- **课程材料** - 材料分类、预览和下载
- **课程作业** - 作业列表、截止时间和下载
- **课程大作业** - 项目要求和优秀范例
- **管理后台** - 静态提示页面

### 交互功能
- **页面跳转** - 完整的路由系统
- **文件下载** - 支持各类课程文件下载
- **响应式导航** - 移动端友好的导航菜单
- **状态管理** - 动态筛选和状态更新

## 📁 文件管理

将课程文件按类型放在对应目录下：
```
public/files/
├── materials/          # 课程材料
│   ├── lesson1.pdf
│   ├── lesson2.pdf
│   └── ...
├── assignments/        # 课程作业
│   ├── HW1.zip
│   ├── HW2.zip
│   └── ...
├── projects/          # 课程大作业
│   ├── example1.zip
│   ├── example2.zip
│   └── ...
└── README.md          # 文件管理说明
```

## 📝 添加新文件

添加新的课程文件时，需要：

1. **将文件放入对应目录**
   - 课程材料 → `public/files/materials/`
   - 课程作业 → `public/files/assignments/`
   - 项目范例 → `public/files/projects/`

2. **更新对应页面的静态数据**
   - 材料页面 → `app/materials/page.tsx`
   - 作业页面 → `app/assignments/page.tsx`
   - 项目页面 → `app/projects/page.tsx`

详细操作说明请参考 `public/files/README.md`

## 🌐 访问地址

部署完成后，网站将在以下地址可用：
`https://parasolleaf.github.io/NLU-DL/`

## ⚠️ 重要说明

- **开发分支**: `gh-pages-src` (包含网页源代码)
- **部署分支**: `gh-pages` (构建后覆盖为静态文件)
- **保护分支**: `master` (课程demo代码样例不可修改)

每次推送到 `gh-pages-src` 分支时，GitHub Actions 会：
1. 构建 Next.js 项目
2. 将构建后的静态文件覆盖到 `gh-pages` 分支
3. GitHub Pages 自动更新网站