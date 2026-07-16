import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 指定模型ID
model_id = "Qwen/Qwen1.5-0.5B-Chat"

# 设置设备，优先使用GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"使用的设备是：{device}")

# 加载分词器
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 加载模型，并将其移动到指定设备
model = AutoModelForCausalLM.from_pretrained(model_id).to(device)

print(f"模型与分词加载完成！")

#准备对话输入
messages = [
  {"role": "system", "content": "你是一个智能助手，请根据用户的问题给出回答。"},
  {"role": "user", "content": "你好请介绍你自己"}
]

# 使用分词器的模板格式化输入
text = tokenizer.apply_chat_template(
  messages, 
  tokenize=False,
  add_generation_prompt=True
)

# 编码输入文本
model_inputs = tokenizer([text], return_tensors="pt").to(device)

print("编码后的输入文本:")
print(model_inputs)

# 使用模型生成回答
# max_new_tokens 控制了模型最多能生产多少新的token
generated_ids = model.generate(
  model_inputs.input_ids,
  max_new_tokens=512
)

# 将生成的 Token ID 截取输入部分
# 这样我们只解码模型新生成的部分

generated_ids = [
  output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

# 解码生成的 Token ID
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print("\n模型生成的回答:")
print(response)
