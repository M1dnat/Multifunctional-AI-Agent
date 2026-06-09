# """
# 多功能智能助手 - Gradio 网页端（最终修复版）
# """

# import os
# import math
# from datetime import datetime
# from dotenv import load_dotenv
# import gradio as gr
# from langchain_openai import ChatOpenAI
# from langchain.tools import tool
# from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

# load_dotenv()
# API_KEY = os.getenv("API_KEY")


# # ============== 工具定义 ==============

# @tool
# def get_weather(city: str) -> str:
#     """查询指定城市的天气信息"""
#     weather_db = {
#         "北京": "多云, 15-22℃, 空气质量良",
#         "上海": "晴天, 18-25℃, 空气质量优",
#         "深圳": "小雨, 22-28℃, 空气质量优",
#         "成都": "阴天, 16-23℃, 空气质量良",
#         "杭州": "晴天, 17-24℃, 空气质量优",
#         "广州": "多云, 21-29℃, 空气质量良"
#     }
#     result = weather_db.get(city)
#     if result:
#         return f"{city}的天气：{result}"
#     return f"暂不支持 {city}"


# @tool
# def calculator(expression: str) -> str:
#     """执行数学计算"""
#     try:
#         expression = expression.replace('×', '*').replace('÷', '/')
#         safe_dict = {
#             "sqrt": math.sqrt, "pow": pow, "abs": abs,
#             "pi": math.pi, "e": math.e
#         }
#         result = eval(expression, {"__builtins__": {}}, safe_dict)
#         if isinstance(result, float):
#             if result.is_integer():
#                 result = int(result)
#             else:
#                 result = round(result, 4)
#         return f"{expression} = {result}"
#     except Exception as e:
#         return f"计算出错: {str(e)}"


# @tool
# def get_current_time() -> str:
#     """获取当前时间和日期"""
#     now = datetime.now()
#     weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
#     return now.strftime(f"%Y年%m月%d日 %H:%M:%S {weekdays[now.weekday()]}")


# @tool
# def convert_usd_to_cny(amount: float) -> str:
#     """将美元转换为人民币"""
#     rate = 7.15
#     result = amount * rate
#     return f"{amount}美元 = {result:.2f}人民币"


# @tool
# def search_product(product_name: str) -> str:
#     """搜索产品信息"""
#     products = {
#         "手机": "📱 iPhone 15 ¥5999、小米14 ¥3999、华为Mate60 ¥6999",
#         "笔记本": "💻 MacBook Pro ¥12999、ThinkPad X1 ¥9999、华为MateBook ¥7999",
#         "耳机": "🎧 AirPods Pro ¥1999、Sony WH-1000XM5 ¥2499"
#     }
#     for key, value in products.items():
#         if product_name in key or key in product_name:
#             return value
#     return f"未找到 '{product_name}'"


# # ============== 助手类 ==============

# class SmartAssistant:
#     def __init__(self):
#         if not API_KEY:
#             raise ValueError("请在 .env 文件中设置 API_KEY")
        
#         self.llm = ChatOpenAI(
#             model="Qwen/Qwen2.5-7B-Instruct",
#             base_url="https://api.siliconflow.cn/v1",
#             api_key=API_KEY,
#             temperature=0.7,
#         )
#         self.tools = [get_weather, calculator, get_current_time, convert_usd_to_cny, search_product]
#         self.tools_by_name = {tool.name: tool for tool in self.tools}
    
#     def chat(self, user_input: str) -> str:
#         """处理用户输入"""
#         if not user_input or not user_input.strip():
#             return "请输入问题"
        
#         try:
#             llm_with_tools = self.llm.bind_tools(self.tools)
            
#             messages = [
#                 SystemMessage(content="你是一个智能助手。根据用户问题调用合适的工具，然后基于工具结果用中文友好回答。"),
#                 HumanMessage(content=user_input)
#             ]
            
#             response = llm_with_tools.invoke(messages)
            
#             # 如果有工具调用
#             if hasattr(response, 'tool_calls') and response.tool_calls:
#                 messages.append(response)
                
#                 for tool_call in response.tool_calls:
#                     tool_name = tool_call["name"]
#                     tool_args = tool_call["args"]
                    
#                     if tool_name in self.tools_by_name:
#                         tool_result = self.tools_by_name[tool_name].invoke(tool_args)
#                         messages.append(ToolMessage(
#                             content=str(tool_result),
#                             tool_call_id=tool_call["id"]
#                         ))
                
#                 # 生成最终回复
#                 final_response = self.llm.invoke(messages)
#                 return final_response.content
            
#             return response.content if response.content else "我无法回答这个问题"
            
#         except Exception as e:
#             return f"处理出错: {str(e)}"


# # ============== Gradio 界面 ==============

# assistant = SmartAssistant()

# def respond(message, history):
#     """响应函数"""
#     if not message or not message.strip():
#         return "", history
    
#     response = assistant.chat(message)
    
#     if history is None:
#         history = []
    
#     # 关键修复：使用正确的消息格式
#     history.append((message, response))
    
#     return "", history

# def clear_history():
#     return []

# # 示例
# EXAMPLES = [
#     "北京天气怎么样",
#     "计算 25 * 3",
#     "现在几点了",
#     "100美元等于多少人民币",
#     "搜索手机"
# ]

# # 创建界面
# with gr.Blocks(title="多功能智能助手", theme=gr.themes.Soft()) as demo:
#     gr.Markdown("""
#     # 🧠 多功能智能助手
    
#     **基于 LangChain 工具调用**
    
#     | 功能 | 示例 |
#     |------|------|
#     | ☁️ 天气 | 北京天气怎么样 |
#     | 🧮 计算 | 计算 25 * 3 |
#     | ⏰ 时间 | 现在几点了 |
#     | 💰 货币 | 100美元等于多少人民币 |
#     | 🔍 搜索 | 搜索手机 |
#     """)
    
#     # 关键：不指定 type，使用默认的 tuple 格式
#     chatbot = gr.Chatbot(height=500, label="对话记录")
    
#     with gr.Row():
#         msg = gr.Textbox(
#             label="输入问题",
#             placeholder="例如：北京天气怎么样？",
#             scale=4,
#             lines=2
#         )
#         send_btn = gr.Button("发送", variant="primary", scale=1)
    
#     with gr.Row():
#         clear_btn = gr.Button("清空对话", variant="secondary")
    
#     gr.Examples(examples=EXAMPLES, inputs=msg, label="📋 示例问题")
    
#     # 绑定事件
#     send_btn.click(respond, [msg, chatbot], [msg, chatbot])
#     msg.submit(respond, [msg, chatbot], [msg, chatbot])
#     clear_btn.click(clear_history, None, chatbot)

# if __name__ == "__main__":
#     print("=" * 50)
#     print("🚀 启动多功能智能助手...")
#     print("📍 本地访问: http://localhost:7860")
#     print("=" * 50)
    
#     demo.launch(
#         server_name="0.0.0.0",
#         server_port=7860,
#         share=False
#     )

"""
多功能智能助手 - 修复货币转换版
"""

import os
import math
import re
from datetime import datetime
from dotenv import load_dotenv
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()
API_KEY = os.getenv("API_KEY")

print(f"API_KEY 是否已设置: {bool(API_KEY)}")


# ============== 工具函数 ==============

def get_weather(city: str) -> str:
    """查询天气"""
    weather_db = {
        "北京": "多云, 15-22℃, 空气质量良",
        "上海": "晴天, 18-25℃, 空气质量优",
        "深圳": "小雨, 22-28℃, 空气质量优",
        "成都": "阴天, 16-23℃, 空气质量良",
        "杭州": "晴天, 17-24℃, 空气质量优",
        "广州": "多云, 21-29℃, 空气质量良"
    }
    result = weather_db.get(city)
    if result:
        return f"{city}的天气：{result}"
    return f"暂不支持 {city}，支持：北京、上海、深圳、成都、杭州、广州"


def calculator(expression: str) -> str:
    """计算器"""
    try:
        # 提取表达式
        expr = re.sub(r'[^0-9+\-*/().%]', '', expression)
        expr = expr.replace('×', '*').replace('÷', '/')
        
        # 安全计算
        safe_dict = {
            "sqrt": math.sqrt, "pow": pow, "abs": abs,
            "pi": math.pi, "e": math.e
        }
        result = eval(expr, {"__builtins__": {}}, safe_dict)
        
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 4)
        return f"{expr} = {result}"
    except Exception as e:
        return f"计算出错: {str(e)}"


def get_current_time():
    """获取时间"""
    now = datetime.now()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    return now.strftime(f"%Y年%m月%d日 %H:%M:%S {weekdays[now.weekday()]}")


def convert_usd_to_cny(amount: float) -> str:
    """货币转换"""
    rate = 7.15
    result = amount * rate
    return f"{amount}美元 = {result:.2f}人民币"


def search_product(product_name: str) -> str:
    """搜索产品"""
    products = {
        "手机": "📱 iPhone 15 ¥5999、小米14 ¥3999、华为Mate60 ¥6999",
        "笔记本": "💻 MacBook Pro ¥12999、ThinkPad X1 ¥9999、华为MateBook ¥7999",
        "耳机": "🎧 AirPods Pro ¥1999、Sony WH-1000XM5 ¥2499"
    }
    for key, value in products.items():
        if product_name in key or key in product_name:
            return value
    return f"未找到 '{product_name}'，试试：手机、笔记本、耳机"


# ============== 意图识别和工具调用 ==============

class SmartAssistant:
    def __init__(self):
        if not API_KEY:
            raise ValueError("请在 .env 文件中设置 API_KEY")
        
        self.llm = ChatOpenAI(
            model="Qwen/Qwen2.5-7B-Instruct",
            base_url="https://api.siliconflow.cn/v1",
            api_key=API_KEY,
            temperature=0.3,
            timeout=30,
        )
    
    def chat(self, user_input: str) -> str:
        """处理用户输入"""
        print(f"\n📝 用户输入: {user_input}")
        
        if not user_input or not user_input.strip():
            return "请输入问题"
        
        user_input_lower = user_input.lower()
        
        # 1. 天气查询
        weather_keywords = ["天气", "气温", "温度"]
        if any(kw in user_input_lower for kw in weather_keywords):
            cities = ["北京", "上海", "深圳", "成都", "杭州", "广州"]
            for city in cities:
                if city in user_input:
                    result = get_weather(city)
                    print(f"🔧 调用天气工具 -> {result}")
                    return result
            return get_weather("")
        
        # 2. 计算器
        calc_keywords = ["计算", "等于", "+", "-", "*", "/", "×", "÷"]
        if any(kw in user_input for kw in calc_keywords):
            # 移除"计算"等中文词，保留数字和运算符
            expr = user_input
            for word in ["计算", "等于", "多少"]:
                expr = expr.replace(word, "")
            expr = expr.strip()
            result = calculator(expr)
            print(f"🔧 调用计算工具 -> {result}")
            return result
        
        # 3. 时间查询
        time_keywords = ["时间", "几点", "什么时候", "日期", "星期"]
        if any(kw in user_input_lower for kw in time_keywords):
            result = get_current_time()
            print(f"🔧 调用时间工具 -> {result}")
            return result
        
        # 4. 货币转换（修复版）
        if "美元" in user_input and "人民币" in user_input:
            # 改进的数字提取：支持整数和小数，支持各种格式
            # 匹配如：100、100.5、100.00、100美元
            patterns = [
                r'(\d+\.?\d*)\s*美元',  # "100美元" 或 "100.5美元"
                r'(\d+\.?\d*)美元',      # "100美元"（无空格）
                r'美元\s*(\d+\.?\d*)',   # "美元100"
                r'(\d+\.?\d*)',          # 单纯的数字
            ]
            
            amount = None
            for pattern in patterns:
                match = re.search(pattern, user_input)
                if match:
                    amount = float(match.group(1))
                    break
            
            if amount:
                result = convert_usd_to_cny(amount)
                print(f"🔧 调用货币转换工具: {amount}美元 -> {result}")
                return result
            else:
                return "请告诉我要转换的美元金额，例如：100美元等于多少人民币"
        
        # 5. 产品搜索
        search_keywords = ["搜索", "找", "查询"]
        products_keywords = ["手机", "笔记本", "耳机", "电脑", "平板"]
        
        if any(kw in user_input_lower for kw in search_keywords + products_keywords):
            for product in ["手机", "笔记本", "耳机"]:
                if product in user_input:
                    result = search_product(product)
                    print(f"🔧 调用搜索工具 -> {result}")
                    return result
            return "支持搜索：手机、笔记本、耳机"
        
        # 6. 默认：使用 LLM 回答
        print("🔄 使用 LLM 直接回答...")
        try:
            messages = [
                SystemMessage(content="你是一个友好的智能助手，用中文简短回答问题。"),
                HumanMessage(content=user_input)
            ]
            response = self.llm.invoke(messages)
            print(f"✅ LLM 回复: {response.content[:100]}...")
            return response.content
        except Exception as e:
            print(f"❌ LLM 错误: {e}")
            return f"处理出错: {str(e)}"


# ============== Gradio 界面 ==============

assistant = SmartAssistant()

def respond(message, history):
    """响应函数"""
    print(f"\n{'='*50}")
    print(f"🎯 收到消息: {message}")
    
    if not message or not message.strip():
        return "", history
    
    response = assistant.chat(message)
    print(f"💬 回复: {response}")
    print(f"{'='*50}\n")
    
    if history is None:
        history = []
    
    # Gradio 6.0 字典格式
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})
    
    return "", history

def clear_history():
    print("🗑️ 清空历史")
    return []

# 示例
EXAMPLES = [
    "北京天气怎么样",
    "计算 25 * 3",
    "现在几点",
    "100美元等于多少人民币",
    "搜索手机",
    "今天星期几",
    "50.5美元是多少人民币",  # 新增：测试小数
    "美元100换人民币"        # 新增：测试不同格式
]

# 创建界面
with gr.Blocks(title="多功能智能助手") as demo:
    gr.Markdown("""
    # 🧠 多功能智能助手
    
    直接输入问题，我会自动识别并回答：
    
    | 功能 | 示例 |
    |------|------|
    | ☁️ 天气查询 | 北京天气怎么样 |
    | 🧮 数学计算 | 计算 25 * 3 |
    | ⏰ 时间日期 | 现在几点 / 今天星期几 |
    | 💰 货币转换 | 100美元等于多少人民币 |
    | 🔍 产品搜索 | 搜索手机 |
    """)
    
    chatbot = gr.Chatbot(height=500, label="对话记录")
    
    with gr.Row():
        msg = gr.Textbox(
            label="输入问题",
            placeholder="例如：100美元等于多少人民币",
            scale=4,
            lines=2
        )
        send_btn = gr.Button("发送", variant="primary", scale=1)
    
    with gr.Row():
        clear_btn = gr.Button("清空对话", variant="secondary")
    
    gr.Examples(examples=EXAMPLES, inputs=msg, label="📋 点击快速提问")
    
    send_btn.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(clear_history, None, chatbot)

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 启动多功能智能助手...")
    print("📍 本地访问: http://localhost:7860")
    print("=" * 50)
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )