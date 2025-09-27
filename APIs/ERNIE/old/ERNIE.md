# DP-NLU 百度千帆Demo Notes

old文件夹中demo对应千帆中心的老版本文档，即采用的key为AK/SK形式而非兼容openai sdk版本，兼容openai sdk版本的key为bce开头的一个秘钥见new文件夹。

## 环境要求
要求python3.7+，且环境中有qianfan的第三方库  
在你的conda虚拟环境下，pip install qianfan

## 相关文档
有关百度千帆的，模型api调用，可见网址：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/klqx7b1xf?utm_source=www.meoai.net  
有关百度千帆的Access key获取，可见网址：https://cloud.baidu.com/doc/Reference/s/9jwvz2egb  
使用时，Access key填入ak；Secret key填入sk

注意！此时你直接运行demo可能会遇到error code 17的Open api daily request limit reached用户配额超限的报错。  
这是因为你并没有在百度智能云千帆ModuleBuilder部署过应用，前往ModuleBuilder，网址如下：https://console.bce.baidu.com/qianfan/overview  
在左侧功能栏中找到“应用接入”选项，创建一个应用（名称、功能随便写、下述应用可用的模型保持默认），创建成功应用后，再次运行demo，发现可以执行。