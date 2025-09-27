# NLU-DL
This is a project used to store API call demos and project examples required for the PKU NLU-DL course.

## 项目结构

### .env：用于存储环境变量 (需要自己在项目目录下手动创建一个)
.env存在的目的是为了在源代码中避免显示地调用各个API模型的key，因而选用环境变量的方式通过os.getenv("你的key名称")隐式调用。我们给出了一个样例.env_example，实际使用时请将其重命名为.env。具体的，.env其内可包含类似如下的key-value定义：  
```env
QWEN_API_KEY=your_api_key_here
DOUBAO_API_KEY=your_api_key_here
```

同时也需要与.env对应的加载环境变量，我们通过调用python-dotenv和pathlib依赖库，在os.getenv()前先进行：  
```
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / '.env'  # 根据实际路径调整
load_dotenv()
```
其中dotenv_path需要根据你实际的文件结构进行调整，Path(__file__).resolve()得到的是你当前.py程序的绝对路径，.parent则是该路径的上一级父目录，以下述目录结构为例：  
├── A/     
│   ├── .env                  
│   └── B/  
│       └── main.py                  
└── .env                
B目录下的main.py中的Path(__file__).resolve()得到的是"./A/B/main.py"，通过一次.parent操作得到的路径为"./A/B"，因此若想使用A目录下的.env文件则需两次.parent操作后链接".env"，若想调用最外层的.env则需三次.parent操作。当然如果发现始终调整不对，你可以显示地在程序中print(dotenv_path)看看你现在的路径节点在哪。  

对于类似ERNIE等非openai接口需要通过POST,GET请求头方式调用的大模型，你也可以通过命名变量auth_token=os.getenv("你的key名称")，后在Headers中拼接的方式隐式调用：  
```
auth_token = os.getenv("ERNIE_NEW_API_KEY")
headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {auth_token}"
    }
```

### APIs: 各个大模型的API调用示例
├── doubao/                 # 豆包API调用，其model需使用控制台下的model_id而非接入点模型名称  
├── ERNIE/                  # 百度千帆相关API调用  
│   ├── img/                # new/中对应生成的图片  
│   ├── new/                # 新版API接口，秘钥为Bearer bceXXX格式，兼容openai接口  
│   └── old/                # 旧版API接口，秘钥为AK/SK格式  
├── net/                    # baidusearch搜索引擎接口，和网络request与beautifulsoup调用  
├── qwen/                   # qwen相关API调用，ipynb包括几个case                     
├── xunfei/                 # 讯飞星火API调用，为spark_ai接口，不兼容openai接口  
└── zhipu/                  # 智谱清言API调用，为zhipuai接口，同时兼容openai接口  
        
### 24point: API调用大模型进行24点
├── 24point_direct.py       # 使用qwen-plus但不开启推理模式  
└── 24point_reason.py       # 使用qwen-plus开启推理模式  

### news: 综合任务可进行网页搜索的大模型调用
├── news_simple.py          # 直接使用大模型不进行网页查询  
├── news_search.py          # 直接使用网页查询，并将查询结果输入大模型  
├── news_decision.py        # 由大模型根据自己的内部知识和问题，决定是否需要网页查询，对应问题是需要查询的  
└── news_decision2.py       # 由大模型根据自己的内部知识和问题，决定是否需要网页查询，对应问题是不需要查询的，与news_decision.py代码相同  

### Sentiment_Analysis: API调用大模型进行情感分析
├── config.py               # 配置文件  
├── sentiment_analysis.py   # 主程序入口  
├── sentiment_analyzer.py   # 情感分析核心类  
├── utils.py                # 工具函数  
├── requirements.txt        # 依赖包  
└── README.md               # 说明文档  

### wereWolves: 综合任务AI狼人杀
├── config/  
│   └── models_config.py    # 模型配置  
├── models/  
│   ├── ai_client.py        # AI客户端统一接口  
│   └── player.py           # 玩家类  
├── game/  
│   ├── game_state.py       # 游戏状态管理  
│   └── werewolf_game.py    # 游戏主逻辑  
├── main.py                 # 主程序入口  
├── requirements.txt        # 依赖包  
└── README.md               # 说明文档  

### projects: 往届优秀作业
├── group4/                 # 智能旅游规划  
├── group8/                 # 多智能语言教学  
└── publish soon ...        # 后续持续更新，敬请期待  

## 项目使用
### 环境配置
建议使用python>=3.10，后根据requirements.txt中依赖库进行安装。  
```
conda create -n test python=3.12
pip install -r requirements.txt
```

### API_KEY及路径配置
请先将.env_example重命名为.env，并根据实际情况修改其中所使用的api_key，相关注册网址已给出，例如：
```
QWEM_API_KEY= sk-XXX    # 无需添加引号
```
若修改了.env在项目中的相对路径，请根据前文的dotenv_path的设置同步进行调整。  