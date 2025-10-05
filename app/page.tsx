import { Navigation } from "@/components/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Calendar, Clock, Users, BookOpen, Award, ChevronRight } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      {/* Hero Section */}
      <section className="relative py-20 px-4 bg-gradient-to-br from-primary/5 to-secondary/5">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-6">
            <Badge variant="secondary" className="mb-4">
              2025 秋 • 信息科学技术学院
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold text-balance">
              基于深度学习的自然语言理解
            </h1>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mt-8">
              <Button size="lg" asChild>
                <Link href="/materials">
                  课程材料
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link href="/assignments">课程作业</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Course Info Grid */}
      <section className="py-16 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">课程日期</CardTitle>
                <Calendar className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">周五</div>
                <p className="text-xs text-muted-foreground">下午3:10-5:00</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">课程</CardTitle>
                <Clock className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">15 周</div>
                <p className="text-xs text-muted-foreground">2025.9 - 2026.1</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">课程人数</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">37</div>
                <p className="text-xs text-muted-foreground">人次</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">学分</CardTitle>
                <Award className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">2</div>
                <p className="text-xs text-muted-foreground">学分/学时</p>
              </CardContent>
            </Card>
          </div>

          {/* Course Description */}
          <div className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BookOpen className="h-5 w-5" />
                    课程描述
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-muted-foreground leading-relaxed">
                    本高级课程全面涵盖自然语言理解的深度学习方法。
                    学生将探索最先进的神经架构，包括Transformer、
                    注意力机制和大型语言模型。
                    课程主页：https://parasolleaf.github.io/NLU-DL/。
                    课程代码demo：https://github.com/ParasolLeaf/NLU-DL。
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Instructor & TA Info */}
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>授课教授</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-semibold">邓志鸿教授</h4>
                      <p className="text-sm text-muted-foreground">北京大学智能学院</p>
                    </div>
                    <div className="text-sm space-y-1">
                      <p>
                        <strong>办公室:</strong> 理科二号楼 2318
                      </p>
                      <p>
                        <strong>邮件:</strong> zhdeng@pku.edu.cn
                      </p>
                      <p>
                        <strong>Office Hours:</strong> ---
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>助教</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-semibold">吴宇桐</h4>
                      <p className="text-sm text-muted-foreground">博士一年级</p>
                      <p className="text-xs">wuyt25@stu.pku.edu.cn</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="h-6 w-6 rounded-full bg-primary flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-xs">PKU</span>
              </div>
              <span className="text-sm text-muted-foreground">Peking University • EECS</span>
            </div>
            <p className="text-sm text-muted-foreground">
              © 2025 Natural Language Understanding based on Deep Learning. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
