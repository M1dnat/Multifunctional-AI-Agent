# 🧠 多功能智能助手 (Multifunctional AI Agent)

基于 LangChain 和 Gradio 构建的智能对话助手，支持天气查询、数学计算、时间查询、货币转换、产品搜索等多种实用功能。

## ✨ 功能特性

| 功能 | 描述 | 示例 |
|------|------|------|
| ☁️ 天气查询 | 查询主要城市天气信息 | "北京天气怎么样" |
| 🧮 数学计算 | 支持基本数学运算 | "计算 25 * 3" |
| ⏰ 时间日期 | 获取当前时间和星期 | "现在几点" |
| 💰 货币转换 | 美元兑人民币转换 | "100美元等于多少人民币" |
| 🔍 产品搜索 | 搜索电子产品信息 | "搜索手机" |

## 🚀 快速开始

### 环境要求

- Python 3.11+
- SiliconFlow API Key

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/M1dnat/Multifunctional-AI-Agent.git
cd Multifunctional-AI-Agent

2. 安装依赖
pip install gradio langchain langchain-openai python-dotenv

3. 配置 API Key
echo "API_KEY=your_api_key_here" > .env

4. 运行应用
python app.py

5. 访问界面
浏览器打开 http://localhost:7860

## 📦 依赖项

gradio>=6.0.0
langchain>=0.2.0
langchain-openai>=0.1.0
python-dotenv>=1.0.0

## 🔧 配置说明

### API 配置

self.llm = ChatOpenAI(
    model="Qwen/Qwen2.5-7B-Instruct",
    base_url="https://api.siliconflow.cn/v1",
    api_key=API_KEY,
    temperature=0.7,
)

### 端口配置

demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False
)

## 🌐 公网访问

### 使用 Cpolar

cpolar http 7860

### 使用 Gradio Share

demo.launch(share=True)

## 📝 使用示例

用户: 北京天气怎么样
助手: 北京的天气：多云, 15-22℃, 空气质量良

用户: 计算 25 * 3
助手: 25*3 = 75

用户: 现在几点
助手: 2026年06月09日 14:30:25 星期二

用户: 100美元等于多少人民币
助手: 100美元 = 715.00人民币

用户: 搜索手机
助手: 📱 iPhone 15 ¥5999、小米14 ¥3999、华为Mate60 ¥6999

## 📁 项目结构

smart-assistant/
├── app.py
├── .env
├── requirements.txt
└── README.md

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request
