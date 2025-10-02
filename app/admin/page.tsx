import { Navigation } from "@/components/navigation"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CircleAlert as AlertCircle } from "lucide-react"

export default function AdminPage() {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <section className="py-12 px-4 bg-gradient-to-r from-primary/5 to-secondary/5">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold text-balance">管理后台</h1>
          </div>
        </div>
      </section>

      <section className="py-12 px-4">
        <div className="container mx-auto max-w-6xl">
          <Card className="max-w-2xl mx-auto">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-muted-foreground" />
                静态网站模式
              </CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription className="text-base leading-relaxed">
                此网站已配置为静态展示模式，管理功能在GitHub Pages环境下不可用。
                <br /><br />
                如需使用完整的管理功能，请在本地环境或支持服务器端功能的平台上部署。
              </CardDescription>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  )
}
