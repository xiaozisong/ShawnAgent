"""
第三章 第1题 课后习题
使用迷你语料库计算 Bigram 概率
语料库: "datawhale agent learns datawhale agent works"
目标: 计算 P("agent works")
"""
import collections

# 语料库
corpus = "datawhale agent learns datawhale agent works"
tokens = corpus.split()
total_tokens = len(tokens)
print(f"语料库: {corpus}")
print(f"总词数: {total_tokens}")
print(f"分词结果: {tokens}\n")

# --- 第一步: P(agent) ---
count_agent = tokens.count('agent')
p_agent = count_agent / total_tokens
print(f"第一步: P(agent) = {count_agent}/{total_tokens} = {p_agent:.4f}")

# --- 第二步: P(works | agent) ---
# 先统计所有 Bigram
bigrams = list(zip(tokens, tokens[1:]))
bigram_counts = collections.Counter(bigrams)
print(f"\n所有 Bigram 及其频次:")
for bg, count in bigram_counts.items():
    print(f"  {bg} → {count} 次")

count_agent_works = bigram_counts[('agent', 'works')]
p_works_given_agent = count_agent_works / count_agent
print(f"\n第二步: P(works | agent) = Count(agent,works) / Count(agent) = {count_agent_works}/{count_agent} = {p_works_given_agent:.4f}")

# --- 最终: 连乘 ---
p_agent_works = p_agent * p_works_given_agent
print(f"\n最终: P('agent works') = P(agent) × P(works|agent) = {p_agent:.4f} × {p_works_given_agent:.4f} = {p_agent_works:.4f}")

# --- 额外: 顺便算一下书中原来的例子做对比 ---
p_datawhale = tokens.count('datawhale') / total_tokens
p_agent_given_datawhale = bigram_counts[('datawhale', 'agent')] / tokens.count('datawhale')
p_learns_given_agent = bigram_counts[('agent', 'learns')] / tokens.count('agent')
p_datawhale_agent_learns = p_datawhale * p_agent_given_datawhale * p_learns_given_agent
print(f"\n--- 对照书中例子 ---")
print(f"P('datawhale agent learns') = {p_datawhale:.4f} × {p_agent_given_datawhale:.4f} × {p_learns_given_agent:.4f} = {p_datawhale_agent_learns:.4f}")
print(f"（书上给的参考值: 0.167）")
