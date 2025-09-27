锘?# 智能旅行规划应用

## 项目概述
这是一个智能旅行规划应用，结合了通义千问大模型和网络搜索功能，帮助用户创建个性化的旅行计划。系统包含后端API服务、前端用户界面和多个功能模块，能够根据目的地、旅行天数、兴趣偏好、预算等信息生成详细的旅行计划。

## 功能特点
- ?? 个性化旅行计划生成
- ? 自动获取目的地天气信息
- ?? 景点搜索与推荐功能
- ? 预算规划建议
- ? 行程日期智能安排
- ? 直观易用的用户界面

## 技术栈
- **后端框架**: FastAPI
- **前端界面**: Gradio
- **AI模型**: 通义千问大模型
- **网络搜索**: Playwright + BeautifulSoup
- **异步处理**: asyncio

## 安装指南

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 安装Playwright浏览器
```bash
playwright install
```

### 3. 配置环境变量
创建`.env`文件并添加通义千问API密钥：
```env
QWEN_API_KEY=your_api_key_here
```

## 运行指南

### 启动后端服务
```bash
python main.py
```
后端将在`http://localhost:8000`运行

### 启动前端界面
```bash
python gradio_gui.py
```
前端将在`http://localhost:7860`运行

## 项目结构
```
travel-planner/
├── .gitignore           # Git忽略规则
├── gradio_gui.py        # 前端用户界面
├── main.py              # FastAPI后端主程序
├── requirements.txt     # Python依赖列表
├── modules/
│   ├── draft_tour.py    # 景点搜索模块
│   ├── draft_weather.py # 天气搜索模块
│   ├── preprocessing.py # 输入预处理
│   ├── qwen_integration.py # 通义千问集成
│   └── travel_service.py # 旅行计划生成服务
```

## 使用说明
1. 访问前端界面 `http://localhost:7860`
2. 填写旅行信息：
   - 目的地
   - 旅行天数（1-10天）
   - 兴趣偏好（如美食、历史、自然等）
   - 预算范围（经济型/舒适型/豪华型）
   - 出发日期（YYYY-MM-DD格式）
   - 可选：启用景点搜索并指定数量
3. 点击"生成旅行计划"按钮
4. 查看生成的个性化旅行计划

## 注意事项
1. 请确保已获得有效的通义千问API密钥
2. 首次运行需要安装Playwright浏览器（执行`playwright install`）
3. 天气和景点搜索功能依赖网络连接
4. 生成详细计划可能需要较长时间（1-2分钟）
5. 建议在启用了景点搜索功能时设置景点数量为5-10个
