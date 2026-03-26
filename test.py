from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from gensim.models import Word2Vec
import matplotlib.font_manager as fm
from adjustText import adjust_text
import warnings

warnings.filterwarnings('ignore')


def visualize_word_vectors_pca(model_path, words=None, n_words=10, figsize=(12, 10),
                               save_path=None, title="词向量分布可视化 (PCA)",
                               random_colors=True, show_arrows=True):

    #  加载模型
    try:
        model = Word2Vec.load(model_path)
        print(f"✓ 模型加载成功，词表大小: {len(model.wv)}")
    except Exception as e:
        print(f"✗ 模型加载失败: {e}")
        return None

    # 选择要可视化的词
    if words is None:
        # 从词表中随机选择n_words个词
        all_words = list(model.wv.key_to_index.keys())

        # 过滤掉过短的词
        valid_words = [w for w in all_words if len(w) >= 2]

        if len(valid_words) < n_words:
            n_words = len(valid_words)
            print(f"警告: 词表有效词不足，只显示{n_words}个词")

        # 随机选择
        np.random.seed(42)  # 设置随机种子以保证可重复性
        selected_indices = np.random.choice(len(valid_words), n_words, replace=False)
        words = [valid_words[i] for i in selected_indices]

    # 过滤掉不在词表中的词
    words = [w for w in words if w in model.wv]

    if not words:
        print("✗ 没有词在词表中")
        return None

    print(f"✓ 将可视化 {len(words)} 个词: {words}")

    # 获取词向量
    vectors = []
    valid_words = []

    for word in words:
        try:
            vector = model.wv[word]
            vectors.append(vector)
            valid_words.append(word)
        except:
            print(f"  跳过词 '{word}' (不在词表中)")

    vectors = np.array(vectors)
    print(f"✓ 获取了 {len(vectors)} 个词向量，形状: {vectors.shape}")

    #使用PCA降维到2D
    pca = PCA(n_components=2, random_state=42)
    vectors_2d = pca.fit_transform(vectors)

    print(f"✓ PCA降维完成，解释方差比: {pca.explained_variance_ratio_}")
    print(f"  总解释方差: {sum(pca.explained_variance_ratio_):.2%}")

    # 创建可视化
    fig, ax = plt.subplots(figsize=figsize)

    # 设置中文字体
    try:
        font_path = None
        for font in fm.fontManager.ttflist:
            if 'SimHei' in font.name or 'Microsoft YaHei' in font.name or 'Heiti' in font.name:
                font_path = font.fname
                break

        if font_path:
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
            plt.rcParams['axes.unicode_minus'] = False
    except:
        pass

    # 准备颜色
    if random_colors:
        colors = plt.cm.rainbow(np.linspace(0, 1, len(valid_words)))
    else:
        colors = ['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2',
                  '#EF476F', '#FFD166', '#118AB2', '#06D6A0', '#073B4C'][:len(valid_words)]

    # 绘制散点
    scatter = ax.scatter(vectors_2d[:, 0], vectors_2d[:, 1],
                         c=colors, s=200, alpha=0.8, edgecolors='white', linewidth=2)

    # 添加文本标签
    texts = []
    for i, word in enumerate(valid_words):
        # 添加文本
        text = ax.text(vectors_2d[i, 0], vectors_2d[i, 1], word,
                       fontsize=12, ha='center', va='center',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                 alpha=0.8, edgecolor=colors[i], linewidth=2))
        texts.append(text)

        # 添加指向文本的箭头
        if show_arrows:
            ax.annotate('', xy=(vectors_2d[i, 0], vectors_2d[i, 1]),
                        xytext=(vectors_2d[i, 0] * 0.97, vectors_2d[i, 1] * 0.97),
                        arrowprops=dict(arrowstyle='->', color=colors[i], alpha=0.6))

    # 调整文本位置避免重叠
    try:
        adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))
    except:
        print("注意: 未安装adjust_text库，文本标签可能重叠")
        print("安装命令: pip install adjustText")

    # 设置图表属性
    ax.set_xlabel('主成分 1', fontsize=14)
    ax.set_ylabel('主成分 2', fontsize=14)
    ax.set_title(title, fontsize=18, pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')

    # 添加主成分解释方差信息
    ax.text(0.02, 0.98, f'解释方差: {sum(pca.explained_variance_ratio_):.2%}',
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.legend([f'词向量 (n={len(valid_words)})'], loc='lower right', fontsize=12)

    plt.tight_layout()

    # 保存或显示
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 可视化已保存到: {save_path}")

    plt.show()

    # 返回额外信息
    result = {
        'words': valid_words,
        'vectors_2d': vectors_2d,
        'pca': pca,
        'fig': fig,
        'ax': ax
    }

    return result

if __name__ == "__main__":
    result = visualize_word_vectors_pca(
        model_path="word2vec.model",  # 替换为您的模型路径
        words=['中国', '美国', '日本', '北京', '上海',
               '东京', '华盛顿', '密西西比河', '长江', '纽约'],
        figsize=(14, 12),
        title="国家城市河流相关词向量分布",
        save_path="word_vectors_pca.png"
    )

    if result:
        print(f"使用的词: {result['words']}")
        print(f"PCA解释方差: {sum(result['pca'].explained_variance_ratio_):.2%}")
