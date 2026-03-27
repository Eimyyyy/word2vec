# word2vec
# 0.环境要求
python3.11

依赖：requirements.txt

# 1.数据来源
https://dumps.wikimedia.org/zhwiki/20260301/zhwiki-20260301-pages-articles-multistream1.xml-p1p187712.bz2

# 2.代码介绍
read_bz2.py检查数据形式

bz2_to_txt.py将bz2压缩文件转变成文本格式

clean_text.py将繁体中文转变成简体中文，并去除无关信息

fenci.py利用哈工大停词表进行分词

word2vec.py训练模型

test.py检测模型

# 3.结果
训练好的模型：word2vec.model ; word2vec.model.syn1neg.npy ; word2vec.model.wv.vectors.npy
(备注：模型大于100MB，上传至云盘：(https://pan.quark.cn/s/eddce8df464b)下载到main文件夹中)

运行test.py得到10个词向量的图片
