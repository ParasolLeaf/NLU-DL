"use client"

import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Download, Calendar, Clock, CircleCheck as CheckCircle } from "lucide-react"
import { useState, useEffect } from "react"

import { CircleAlert as AlertCircle } from "lucide-react"

// 获取文件元数据的函数
async function getFileMetadata(filename: string) {
  try {
    const response = await fetch(`/NLU-DL/files/assignments/${filename}`, { method: 'HEAD' })
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

// 静态作业数据
const staticAssignments = [
  {
    id: "1",
    title: "课程作业1：AG_NEWS分类及信息抽取",
    description: "课程作业主要为了帮助同学们了解大模型api的调用和后续处理方法，体会大模型在自然语言处理任务上的准确性、泛化性，具体要求见附件。\n测试数据在agnews_sample.csv，包含100条测试数据，只需要在该100条数据上完成实验即可，不需要从网络上下载完整的测试集。",
    type: "assignment",
    ddl: "2025-09-30T15:59:00.000Z",
    uploadDate: null, // 将自动获取
    size: null, // 将自动获取
    filename: "HW1.zip"
  }
]

function calcStatus(dueDateStr: string): "已截止" | "进行中" {
  const due = new Date(dueDateStr).getTime();
  const now = Date.now();
  return now > due ? "已截止" : "进行中";
}

export default function AssignmentsPage() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [assignments, setAssignments] = useState(staticAssignments)
  const [metadataLoading, setMetadataLoading] = useState(true)

  // 在组件挂载时获取文件元数据
  useEffect(() => {
    const loadFileMetadata = async () => {
      const updatedAssignments = await Promise.all(
        staticAssignments.map(async (assignment) => {
          const metadata = await getFileMetadata(assignment.filename)
          return {
            ...assignment,
            uploadDate: metadata.uploadDate,
            size: metadata.size
          }
        })
      )
      setAssignments(updatedAssignments)
      setMetadataLoading(false)
    }

    loadFileMetadata()
  }, [])

  const assignmentFiles = assignments

  const handleDownloadFile = (file: any) => {
    // 直接下载文件
    const link = document.createElement('a')
    link.href = `/NLU-DL/files/assignments/${file.filename}`
    link.download = file.filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  function getStatusColor(status: string) {
    switch (status) {
      case "已截止":
        return "bg-green-500"
      case "进行中":
        return "bg-blue-500"
      default:
        return "bg-gray-400"
    }
  }

  function getStatusIcon(status: string) {
    switch (status) {
      case "已截止":
        return <CheckCircle className="h-4 w-4" />
      case "进行中":
        return <Clock className="h-4 w-4" />
      default:
        return <AlertCircle className="h-4 w-4" />
    }
  }

  if (loading || metadataLoading) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <section className="py-12 px-4 bg-gradient-to-r from-primary/5 to-secondary/5">
          <div className="container mx-auto max-w-6xl">
            <div className="text-center space-y-4">
              <h1 className="text-4xl font-bold text-balance">课程作业</h1>
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

  if (error) {
    return (
      <div className="min-h-screen bg-background">
        <Navigation />
        <div className="flex items-center justify-center py-20">
          <Card className="max-w-md">
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 text-destructive mb-2">
                <AlertCircle className="h-5 w-5" />
                <p className="font-medium">加载失败</p>
              </div>
              <p className="text-sm text-muted-foreground mb-4">{error}</p>
              <Button onClick={() => window.location.reload()} variant="outline" className="w-full">
                重试
              </Button>
            </CardContent>
          </Card>
        </div>
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
            <h1 className="text-4xl font-bold text-balance">课程作业</h1>
          </div>
        </div>
      </section>

      <section className="py-12 px-4">
        <div className="container mx-auto max-w-6xl">
          {/* Assignments List */}
          <div className="space-y-6">
            {assignmentFiles.map((assignment) => {
              const assignmentGuides = assignmentFiles.filter(
                (file) =>
                  file.title.toLowerCase().includes(assignment.title.toLowerCase().split(" ")[0]),
              )

              return (
                <Card key={assignment.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="space-y-3">
                        <div className="flex items-center gap-2">
                          <div className={`w-3 h-3 rounded-full ${getStatusColor(calcStatus(assignment.ddl))}`} />
                          <Badge variant="outline" className="capitalize">
                            {getStatusIcon(calcStatus(assignment.ddl))}
                            <span className="ml-1">{calcStatus(assignment.ddl).replace("-", " ")}</span>
                          </Badge>
                          {/* <Badge variant="secondary">{assignment.points} 分</Badge> */}
                        </div>
                        <CardTitle className="text-xl">{assignment.title}</CardTitle>
                        {/* <CardDescription className="text-base">{assignment.description}</CardDescription> */}
                        <CardDescription
                          className="text-base whitespace-pre-line"
                          dangerouslySetInnerHTML={{
                            __html: assignment.description.replace(/\n/g, "<br />"),
                          }}
                        />
                      </div>
                      <div className="flex flex-col gap-2">
                        {assignmentGuides.map((file) => (
                          <Button key={file.id} size="sm" onClick={() => handleDownloadFile(file)}>
                            <Download className="h-4 w-4 mr-2" />
                            下载作业
                          </Button>
                        ))}
                        {assignmentGuides.length === 0 && (
                          <Button size="sm" disabled>
                            <Download className="h-4 w-4 mr-2" />
                            作业还未发布
                          </Button>
                        )}
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-3 gap-4 text-sm">
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <span>DDL: {new Date(assignment.ddl).toLocaleDateString()}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <span>发布: {assignment.uploadDate ? new Date(assignment.uploadDate).toLocaleDateString() : '未知'}</span>
                      </div>
                      <div className="text-xs bg-muted px-2 py-1 rounded w-fit">
                        {assignment.size ? (assignment.size / 1024 / 1024).toFixed(1) : '0'} MB
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>
    </div>
  )
}
