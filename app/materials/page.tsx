import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { FileText, Download, Calendar, Eye } from "lucide-react"

// 静态课程材料数据
const staticMaterials = [
  {
    id: "1",
    title: "Lesson 1 - 课程介绍",
    description: "课程概述、学习目标和基础概念介绍",
    type: "lecture",
    uploadDate: "2025-09-22T08:21:22.334Z",
    size: 4009521,
    filename: "lesson1.pdf"
  }
]

export default function MaterialsPage() {
  const materials = staticMaterials
  const activeFilter = "全部"

  const materialTypes = [
    { type: "全部", count: materials.length },
    { type: "课件", count: materials.filter((m) => m.type === "lecture").length },
    { type: "阅读材料", count: materials.filter((m) => m.type === "reading").length },
    { type: "补充材料", count: materials.filter((m) => m.type === "supplementary").length },
  ]

  const filteredMaterials = materials

  const handleDownload = (material: any) => {
    // 在静态模式下，显示提示信息
    alert("文件下载功能在静态网站模式下不可用")
  }

  const handlePreview = (material: any) => {
    // 在静态模式下，显示提示信息
    alert("文件预览功能在静态网站模式下不可用")
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
                          {new Date(material.uploadDate).toLocaleDateString()}
                        </div>
                      </div>
                      <div className="text-xs bg-muted px-2 py-1 rounded">
                        {(material.size / 1024 / 1024).toFixed(1)} MB
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
