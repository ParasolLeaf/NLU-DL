# 课程文件管理说明

本目录用于存放所有课程相关文件，按照功能模块进行分类管理。

## 📁 目录结构

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
└── README.md          # 本说明文件
```

## 🔧 添加新文件的操作流程

### 1. 添加课程材料 (Materials)

**步骤1**: 将文件放入对应目录
```bash
# 将新的课程材料放入 materials 目录
public/files/materials/lesson3.pdf
```

**步骤2**: 更新 `app/materials/page.tsx` 中的静态数据
```javascript
const staticMaterials = [
  // 现有材料...
  {
    id: "3",  // 新的唯一ID
    title: "Lesson 3 - 新课程标题",
    description: "课程描述",
    type: "lecture", // lecture/reading/supplementary
    uploadDate: "2025-01-15T08:00:00.000Z", // 上传日期
    size: 5000000, // 文件大小(字节)
    filename: "lesson3.pdf" // 文件名(需与实际文件名一致)
  }
]
```

### 2. 添加课程作业 (Assignments)

**步骤1**: 将文件放入对应目录
```bash
# 将新的作业文件放入 assignments 目录
public/files/assignments/HW2.zip
```

**步骤2**: 更新 `app/assignments/page.tsx` 中的静态数据
```javascript
const staticAssignments = [
  // 现有作业...
  {
    id: "2",  // 新的唯一ID
    title: "课程作业2：新作业标题",
    description: "作业描述和要求",
    type: "assignment",
    ddl: "2025-02-15T23:59:00.000Z", // 截止日期
    uploadDate: "2025-01-20T10:00:00.000Z", // 发布日期
    filename: "HW2.zip" // 文件名(需与实际文件名一致)
  }
]
```

### 3. 添加项目范例 (Projects)

**步骤1**: 将文件放入对应目录
```bash
# 将新的项目范例放入 projects 目录
public/files/projects/example3.zip
```

**步骤2**: 更新 `app/projects/page.tsx` 中的静态数据
```javascript
const staticExampleFiles = [
  // 现有范例...
  {
    id: "3",  // 新的唯一ID
    title: "优秀范例 3",
    description: "项目描述",
    type: "example",
    filename: "example3.zip" // 文件名(需与实际文件名一致)
  }
]
```

## 📋 文件命名规范

### 课程材料 (Materials)
- **课件**: `lesson{N}.pdf` (如: lesson1.pdf, lesson2.pdf)
- **阅读材料**: `reading{N}.pdf` (如: reading1.pdf)
- **补充材料**: `supplement{N}.pdf` (如: supplement1.pdf)

### 课程作业 (Assignments)
- **作业文件**: `HW{N}.zip` (如: HW1.zip, HW2.zip)
- **作业说明**: `HW{N}_instruction.pdf` (如: HW1_instruction.pdf)

### 项目范例 (Projects)
- **优秀范例**: `example{N}.zip` (如: example1.zip, example2.zip)
- **项目要求**: `project_requirements.pdf`

## ⚠️ 重要注意事项

1. **文件名一致性**: 确保代码中的 `filename` 字段与实际文件名完全一致
2. **文件大小**: 建议在代码中填写准确的文件大小(字节)，便于用户了解下载大小
3. **日期格式**: 使用 ISO 8601 格式 (`YYYY-MM-DDTHH:mm:ss.sssZ`)
4. **唯一ID**: 每个文件条目必须有唯一的ID
5. **文件类型**: 
   - Materials: `lecture`(课件) / `reading`(阅读材料) / `supplementary`(补充材料)
   - Assignments: `assignment`
   - Projects: `example`

## 🚀 部署流程

添加文件后的完整流程：

1. **添加文件到对应目录**
2. **更新对应页面的静态数据**
3. **提交代码**
   ```bash
   git add .
   git commit -m "Add new course files"
   git push origin gh-pages-src
   ```
4. **等待自动部署完成**
5. **测试文件下载功能**

## 📞 技术支持

如果遇到问题，请检查：
- 文件路径是否正确
- 文件名是否与代码中一致
- 静态数据是否正确更新
- GitHub Actions 是否成功部署