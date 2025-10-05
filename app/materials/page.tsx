"use client"

import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { FileText, Download, Calendar, Eye } from "lucide-react"
import { useState, useEffect } from "react"

// 静态课程材料数据
const staticMaterials = [
  {
    id: "1",
    title: "Lesson 1",
    description: "课程简介、自然语言理解与语言模型",
    type: "lecture",
    uploadDate: "2025-09-12", // 手动设置日期，格式：YYYY-MM-DD
    size: null, // 将自动获取
    filename: "lesson1.pdf"
  },
  {
    id: "2",
    title: "Lesson 2",
    description: "神经语言模型与词嵌入",
    type: "lecture",
    uploadDate: "2025-09-19", // 自动获取文件修改时间
    size: null, // 将自动获取
    filename: "lesson2.pdf"
  },
  {
    id: "3",
    title: "2025 Reading List",
    description: "2025年论文阅读清单",
    type: "reading",
    uploadDate: "2025-09-26", // 将自动获取
    size: null, // 将自动获取
    filename: "2025_Reading_List.zip"
  },
  {
    id: "4",
    title: "2025 课程项目介绍",
    description: "2025年课程项目介绍，包含基本的api调用说明与项目要求，包含的样例代码在github仓库master分支中，链接见https://github.com/ParasolLeaf/NLU-DL",
    type: "supplementary",
    uploadDate: "2025-09-19", // 将自动获取
    size: null, // 将自动获取
    filename: "project_intro.pdf"
  },
  {
    id: "5",
    title: "conda 环境配置",
    description: "conda环境配置参考文档，及相关错误解决方案和参考.condarc文件",
    type: "supplementary",
    uploadDate: "2025-09-19", // 将自动获取
    size: null, // 将自动获取
    filename: "conda.zip"
  }
]

// 获取文件元数据的函数
async function getFileMetadata(filename: string) {
  try {
    const response = await fetch(`/NLU-DL/files/materials/${filename}`, { method: 'HEAD' })
    if (response.ok) {
      const lastModified = response.headers.get('last-modified')
      const contentLength = response.headers.get('content-length')
      
      return {
        uploadDate: lastModified ? new Date(lastModified).toISOString() : new Date().toISOString(),
        size: contentLength ? parseInt(contentLength) : 0
      }
    }
  } catch (error) {
    console.warn(`无法获取文件 ${filename} 的元数据:`, error)
  }
  
  // 返回默认值
  return {
    uploadDate: new Date().toISOString(),
    size: 0
  }
}
export default function MaterialsPage() {
  const [activeFilter, setActiveFilter] = useState("全部")
  const [materials, setMaterials] = useState(staticMaterials)
  const [loading, setLoading] = useState(true)

  // 在组件挂载时获取文件元数据
  useEffect(() => {
    const loadFileMetadata = async () => {
      const updatedMaterials = await Promise.all(
        staticMaterials.map(async (material) => {
          // 如果有预定义的uploadDate，转换为ISO格式
          const predefinedDate = material.uploadDate ? 
            new Date(material.uploadDate + 'T00:00:00.000Z').toISOString() : 
            null
          
          const metadata = await getFileMetadata(material.filename, predefinedDate)
          return {
            ...material,
            uploadDate: metadata.uploadDate,
            size: metadata.size
          }
        })
      )
      setMaterials(updatedMaterials)
      setLoading(false)
    }

    loadFileMetadata()
  }, [])

  const materialTypes = [
    { type: "全部", count: materials.length },
    { type: "课件", count: materials.filter((m) => m.type === "lecture").length },
    { type: "阅读材料", count: materials.filter((m) => m.type === "reading").length },
    { type: "补充材料", count: materials.filter((m) => m.type === "supplementary").length },
  ]

  const filteredMaterials = activeFilter === "全部" 
    ? materials 
    : materials.filter((material) => {
        if (activeFilter === "课件") return material.type === "lecture"
        if (activeFilter === "阅读材料") return material.type === "reading"
        if (activeFilter === "补充材料") return material.type === "supplementary"
        return true
      })

  const handleDownload = (material: any) => {
    // 直接下载文件
    const link = document.createElement('a')
    link.href = `/NLU-DL/files/materials/${material.filename}`
    link.download = material.filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const handlePreview = (material: any) => {
    // 在新窗口打开文件
    window.open(`/NLU-DL/files/materials/${material.filename}`, '_blank')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <section className="py-12 px-4 bg-gradient-to-r from-primary/5 to-secondary/5">
          <div className="container mx-auto max-w-6xl">
            <div className="text-center space-y-4">
              <h1 className="text-4xl font-bold text-balance">课程材料</h1>
            </div>
          </div>
        </section>
        <section className="py-12 px-4">
          <div className="container mx-auto max-w-6xl">
            <div className="text-center">
              <p className="text-lg text-muted-foreground">正在加载文件信息...</p>
            </div>
          </div>
        </section>
      </div>
    )
  }
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      {/* Header */}
      <section className="py-12 px-4 bg-gradient-to-r from-primary/5 to-secondary/5">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold text-balance">课程材料</h1>
          </div>
        </div>
      </section>

      <section className="py-12 px-4">
        <div className="container mx-auto max-w-6xl">
          {/* Filter Tabs */}
          <div className="flex flex-wrap gap-2 mb-8">
            {materialTypes.map((filter) => (
              <Badge
                key={filter.type}
                variant={activeFilter === filter.type ? "default" : "secondary"}
                className="px-4 py-2 cursor-pointer hover:bg-secondary/80"
                onClick={() => setActiveFilter(filter.type)}
              >
                {filter.type} ({filter.count})
              </Badge>
            ))}
          </div>

          {/* Materials Grid */}
          <div className="grid gap-6">
            {filteredMaterials.length === 0 ? (
              <Card className="text-center py-12">
                <CardContent>
                  <p className="text-lg text-muted-foreground">暂无材料</p>
                </CardContent>
              </Card>
            ) : (
              filteredMaterials.map((material) => (
                <Card key={material.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <Badge
                            variant={
                              material.type === "lecture"
                                ? "default"
                                : material.type === "reading"
                                  ? "secondary"
                                  : "outline"
                            }
                          >
                            {material.type === "lecture"
                              ? "课件"
                              : material.type === "reading"
                                ? "阅读材料"
                                : "补充材料"}
                          </Badge>
                        </div>
                        <CardTitle className="text-xl">{material.title}</CardTitle>
                        <CardDescription className="text-base">{material.description}</CardDescription>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button variant="outline" size="sm" onClick={() => handlePreview(material)}>
                          <Eye className="h-4 w-4 mr-2" />
                          预览
                        </Button>
                        <Button size="sm" onClick={() => handleDownload(material)}>
                          <Download className="h-4 w-4 mr-2" />
                          下载
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between text-sm text-muted-foreground">
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-1">
                          <FileText className="h-4 w-4" />
                          {material.filename.split(".").pop()?.toUpperCase()}
                        </div>
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          {material.uploadDate ? new Date(material.uploadDate).toLocaleDateString() : '未知'}
                        </div>
                      </div>
                      <div className="text-xs bg-muted px-2 py-1 rounded">
                        {material.size ? (material.size / 1024 / 1024).toFixed(1) : '0'} MB
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>
      </section>
    </div>
  )
}
