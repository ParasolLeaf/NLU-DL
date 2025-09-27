# DP-NLU 星火认知Demo Notes
## 环境配置
python3.8+， 装有spark_ai_python库  
在虚拟环境中，pip install --upgrade spark_ai_python

## 相关文档信息
有关api调用文档，可见网址：https://www.xfyun.cn/doc/spark/Web.html  
各个星火认知大模型的URL值，可见网址：https://www.xfyun.cn/doc/spark/Web.html  
Access Key获取，可见网址：https://console.xfyun.cn/services/bm35  
各个星火认知大模型的domain值，可见网址：https://www.xfyun.cn/doc/spark/Web.html  

## 请在尝试运行demo前，完成以下步骤，否则会报错appid没有权限
1. 类似百度千帆大模型，需要先创建一个应用，在控制台右上角用户菜单下选择我的应用，
   或直接通过网址打开应用控制台 https://console.xfyun.cn/app/myapp ，在其中创建你的应用
2. 在创建好应用后，你应该可以看到已创建的应用中有刚创建的应用，双击这个应用，来到这个应用的模型管理控制台，https://console.xfyun.cn/services/sparkapiCenter
3. 此时你可以选择对应的大模型，购买并管理你的token余额。当你想调用的模型token余额为0时，点击立即购买，此时你可以看到相应的套餐包，
   讯飞星火应该是对每个用户均有免费额度的，选择0元的套餐包即可
4. 此时，你已经配置好你的api控制台权限，调用api即可