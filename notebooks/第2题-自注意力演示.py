"""
第三章 第2题 课后练习
最小可运行的自注意力演示
效果: 给定一个句子,可视化每个词对其他词的注意力权重
"""
import torch
import torch.nn.functional as F
import math

# 模拟一个句子
sentence = "The agent learns because it is intelligent".split()
print(f"句子: {sentence}")
print(f"长度: {len(sentence)} 个词\n")

# 设定参数
d_model = 8      # 词嵌入维度（实际中是 512/1024 等大值，这里为方便演示设小）
torch.manual_seed(42)

# 1. 模拟词嵌入（实际中是从预训练模型加载或者通过 nn.Embedding 学习）
embeddings = torch.randn(len(sentence), d_model)
print(f"词嵌入形状: {embeddings.shape}  # (seq_len, d_model)")

# 2. 构造 Q, K, V 三个权重矩阵（实际中是可学习参数）
W_Q = torch.randn(d_model, d_model)
W_K = torch.randn(d_model, d_model)
W_V = torch.randn(d_model, d_model)

# 3. 计算 Q, K, V
Q = embeddings @ W_Q   # (seq_len, d_model)
K = embeddings @ W_K
V = embeddings @ W_V

# 4. 计算注意力分数 (scaled dot-product)
d_k = d_model
scores = Q @ K.T / math.sqrt(d_k)   # (seq_len, seq_len)
print(f"注意力分数矩阵形状: {scores.shape}  # (seq_len, seq_len)")

# 5. Softmax 归一化
attn_weights = F.softmax(scores, dim=-1)

# 6. 加权求和得到融合上下文的新表示
output = attn_weights @ V   # (seq_len, d_model)

# 7. 可视化每个词的注意力分布
print("\n=== 注意力权重矩阵（每行代表当前词对所有词的关注度）===")
header = "        " + "  ".join([f"{w:>7s}" for w in sentence])
print(header)
for i, word in enumerate(sentence):
    row = attn_weights[i].tolist()
    row_str = "  ".join([f"{v:7.3f}" for v in row])
    print(f"{word:>7s}  {row_str}")

print("\n=== 重点观察 'it' 这个词 ===")
it_idx = sentence.index("it")
it_attn = attn_weights[it_idx].tolist()
for word, weight in zip(sentence, it_attn):
    bar = "█" * int(weight * 50)
    print(f"  it → {word:>13s}: {weight:.3f} {bar}")
