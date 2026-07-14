# 导入gradio库并设置别名为gr
import gradio as gr

# # 功能实现
# def reverse_text(text):
#   return text[::-1]

# # 界面配置
# demo = gr.Interface(
#   fn=reverse_text, # 调用reverse_text函数
#   inputs="text", # 输入类型为text
#   outputs="text" # 输出类型为text
# )

# # 启动应用
# demo.launch()


# def reverse_and_count(text):
#   reversed_text = text[::-1]
#   length = len(text)
#   return reversed_text, length

# demo = gr.Interface(
#   fn=reverse_and_count,
#   inputs="text",
#   outputs=["text", "number"],
#   title="文本处理工具",
#   description="输入一段文字，查看其倒序形式及字符数",
#   examples=[["你好，世界"], ["Hello,World!"]]
# )

# demo.launch()

