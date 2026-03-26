from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from gensim.models.callbacks import CallbackAny2Vec
import multiprocessing
import time
import os
from tqdm import tqdm


class EpochLogger(CallbackAny2Vec):

    def __init__(self):
        self.epoch = 0
        self.start_time = time.time()

    def on_epoch_begin(self, model):
        print(f"开始第 {self.epoch + 1} 轮训练...")

    def on_epoch_end(self, model):
        elapsed = time.time() - self.start_time
        print(f"第 {self.epoch + 1} 轮训练完成，耗时: {elapsed:.1f} 秒")
        self.epoch += 1
        self.start_time = time.time()


def train_basic_word2vec(corpus_file, model_path, vector_path=None):

    sentences = LineSentence(corpus_file)

    cores = multiprocessing.cpu_count()

    print("开始训练模型...")
    start_time = time.time()

    model = Word2Vec(
        sentences=sentences,
        vector_size=100,  # 词向量维度
        window=5,  # 上下文窗口大小
        min_count=5,  # 忽略出现次数少于5次的词
        workers=cores,  # 使用多线程
        epochs=5,  # 训练轮数
        sg=1,  # 1: skip-gram, 0: CBOW
        hs=0,  # 0: 使用负采样, 1: 使用层次softmax
        negative=5,  # 负采样数量
        ns_exponent=0.75,  # 负采样指数
        sample=1e-3,  # 高频词下采样阈值
        alpha=0.025,  # 初始学习率
        min_alpha=0.0001,  # 最小学习率
        seed=408,  # 随机种子
        callbacks=[EpochLogger()]  # 训练回调
    )

    training_time = time.time() - start_time
    print(f"模型训练完成!耗时: {training_time / 60:.1f} 分钟")

    #保存模型
    model.save(model_path)

    #保存词向量
    if vector_path:
        print(f"保存词向量到: {vector_path}")
        model.wv.save_word2vec_format(vector_path, binary=False)

    #模型信息
    print(f"\n模型信息:")
    print(f"  词表大小: {len(model.wv)}")
    print(f"  向量维度: {model.vector_size}")
    print(f"  训练轮数: {model.epochs}")
    print(f"  算法: {'Skip-gram' if model.sg else 'CBOW'}")

    return model


model = train_basic_word2vec(
    corpus_file="tokenized_with_stopwords.txt",
    model_path="word2vec.model",
    vector_path="word_vectors.txt"
)