"""
第三章 第3题 课后练习
BPE (Byte-Pair Encoding) 算法手动模拟
"""
import re, collections

def get_stats(vocab):
    """统计词元对频率"""
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols)-1):
            pairs[symbols[i], symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, v_in):
    """合并词元对"""
    v_out = {}
    bigram = re.escape(' '.join(pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in v_in:
        w_out = p.sub(''.join(pair), word)
        v_out[w_out] = v_in[word]
    return v_out

# ---- 第1步: 准备语料库 ----
vocab = {
    'h u g </w>': 1,    # </w> 是词结束标记
    'p u g </w>': 1,
    'p u n </w>': 1,
    'b u n </w>': 1,
}

print("=== BPE 迭代合并过程 ===")
print(f"初始词表大小: 7 (h, u, g, p, n, b, </w>)")
print(f"初始语料: {dict(vocab)}\n")

num_merges = 4
for i in range(num_merges):
    pairs = get_stats(vocab)
    if not pairs:
        break
    
    # 找出频率最高的词元对
    best = max(pairs, key=pairs.get)
    vocab = merge_vocab(best, vocab)
    
    print(f"第{i+1}次合并: {best} -> '{''.join(best)}' (频次: {pairs[best]})")
    print(f"  新词表: {list(vocab.keys())}")

# ---- 第2步: 用训练好的 BPE 规则对新词分词 ----
print("\n=== 对新词进行分词 ===")
# 训练结束后, 用学习到的合并规则来切分新词
# 最终词表中包含: h, p, b, ug, un, ug</w>, un</w>, 以及单个字符

def tokenize_bpe(word, merges):
    """
    用学习到的合并规则分词
    merges: 从合并顺序构建的规则列表
    """
    # 初始切分为字符
    tokens = list(word) + ['</w>']
    # 模拟：按合并优先级尝试合并
    for merge_pair, merge_result in merges.items():
        i = 0
        while i < len(tokens) - 1:
            if tokens[i] == merge_pair[0] and tokens[i+1] == merge_pair[1]:
                tokens = tokens[:i] + [merge_result] + tokens[i+2:]
            else:
                i += 1
    return tokens

# 从上面实验保存合并规则
merges = {
    ('u', 'g'): 'ug',
    ('ug', '</w>'): 'ug</w>',
    ('u', 'n'): 'un',
    ('un', '</w>'): 'un</w>',
}

test_words = ["bug", "hug", "puppy", "bunny"]
for word in test_words:
    tokens = tokenize_bpe(word, merges)
    # 过滤掉 </w>
    clean_tokens = [t for t in tokens if t != '</w>']
    print(f"  {word:>8s} → {clean_tokens}")

print("\n=== 关键观察 ===")
print("'bug' 虽然从未出现在训练语料中，但被分成了 ['b', 'ug']")
print("因为 BPE 学会了: 'ug' 是一个高频子词片段")
print("这就是子词分词的核心优势: 用有限词表组合出无限可能！")
