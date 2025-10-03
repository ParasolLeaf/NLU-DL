"use client"

import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { FileText, Download, Calendar, Lightbulb } from "lucide-react"

// 静态项目数据
const staticProjectFiles = []
const staticExampleFiles = [
  {
    id: "1",
    title: "优秀范例 1",
    description: "往年优秀大作业示例",
    type: "example",
    filename: "example1.zip"
  },
  {
    id: "2", 
    title: "优秀范例 2",
    description: "往年优秀大作业示例",
    type: "example",
    filename: "example2.zip"
  }
]

const projectRequirements = {
  overview: `开放式任务：基于大模型api的任务系统构建
具体要求：
• 参考后续介绍，构思一个可由大模型参与执行的任务
• 实现大模型 API调用
• 构建一个有大模型api参与，可接收输入输出，完成该任务的系统
• 在调用单个大模型的基础上，集成更多功能构建该系统
• 多个大模型角色扮演
• 结合Python 功能（如抓取网页、预处理数据，数据统计分析等）
• 集成其他工具（如图像检测等）
• 比较不同工具/大模型在此任务上的区别

预期成果：
• 简短报告（问题/任务、思路、实现方式、遇到的问题与解决方法，比较分析结果）
• 一个可运行的 Demo（支持输入需求文字、输出结果）
• 现场演示展示基于样例的完整任务流程
我们会提供一个候选课程项目供参考与选择，也可以自己选题形成一个满足上述要求的课程项目。`,
  timeline: [
    { phase: "Proposal", date: "April 15", description: "Submit project proposal with problem statement and approach" },
    { phase: "Milestone", date: "May 1", description: "Present initial results and progress update" },
    { phase: "Final Submission", date: "May 20", description: "Submit complete project with code, report, and presentation" },
    { phase: "Presentations", date: "May 22-24", description: "Present final projects to class" },
  ]
}

export default function ProjectsPage() {
  const projectFiles = staticProjectFiles
  const exampleFiles = staticExampleFiles

  const handleDownloadFile = (file: any) => {
    // 模拟文件下载
    const link = document.createElement('a')
    link.href = `/files/${file.filename}`
    link.download = file.filename
    link.click()
  }
  
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      {/* Header */}
      <section className="py-12 px-4 bg-gradient-to-r from-primary/5 to-secondary/5">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold text-balance">课程大作业</h1>
          </div>
        </div>
      </section>

      <section className="py-12 px-4">
        <div className="container mx-auto max-w-6xl">
          <Tabs defaultValue="requirements" className="space-y-8">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="requirements">大作业要求</TabsTrigger>
              <TabsTrigger value="examples">往年优秀大作业</TabsTrigger>
            </TabsList>

            <TabsContent value="requirements" className="space-y-8">
              {/* Project Overview */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Lightbulb className="h-5 w-5 text-secondary" />
                    概览
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{projectRequirements.overview}</p>
                </CardContent>
              </Card>


              {/* Timeline */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Calendar className="h-5 w-5 text-secondary" />
                    时间线
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {projectRequirements.timeline.map((milestone, idx) => (
                      <div key={idx} className="flex items-start gap-4">
                        <div className="flex flex-col items-center">
                          <div className="w-3 h-3 rounded-full bg-primary" />
                          {idx < projectRequirements.timeline.length - 1 && (
                            <div className="w-0.5 h-12 bg-border mt-2" />
                          )}
                        </div>
                        <div className="flex-1 pb-8">
                          <div className="flex items-center gap-3 mb-2">
                            <h4 className="font-semibold">{milestone.phase}</h4>
                            <Badge variant="secondary">{milestone.date}</Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">{milestone.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Resources */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="h-5 w-5 text-secondary" />
                    资料
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-3 gap-4">
                    {projectFiles.length === 0 ? (
                      <div className="col-span-3 text-center py-8">
                        <p className="text-muted-foreground">暂未发布</p>
                      </div>
                    ) : (
                      projectFiles.map((file) => (
                        <Button
                          key={file.id}
                          variant="outline"
                          className="h-auto p-4 flex flex-col items-center gap-2 bg-transparent"
                          onClick={() => handleDownloadFile(file)}
                        >
                          <Download className="h-5 w-5" />
                          <span>{file.title}</span>
                          <span className="text-xs text-muted-foreground">{file.description}</span>
                        </Button>
                      ))
                    )}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="examples" className="space-y-8">
              {/* Filter */}

              {/* Excellent Projects */}
              <div className="grid gap-6">
                {exampleFiles.map((project) => (
                  <Card key={project.id} className="hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="space-y-3 flex-1">
                          <CardTitle className="text-xl">{project.title}</CardTitle>
                          <CardDescription className="text-base">{project.description}</CardDescription>
                        </div>
                        <div className="ml-4">
                          <Button size="sm" onClick={() => handleDownloadFile(project)}>
                            <Download className="h-4 w-4 mr-2" />
                            下载
                          </Button>
                        </div>
                      </div>
                    </CardHeader>
                  </Card>
                ))}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </section>
    </div>
  )
}
