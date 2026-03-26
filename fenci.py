#进行分词
import jieba
from tqdm import tqdm


def tokenize_with_stopwords(input_file, output_file, stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as f:
        stopwords = set([line.strip() for line in f if line.strip()])

    with open(input_file, 'r', encoding='utf-8') as f_in, \
            open(output_file, 'w', encoding='utf-8') as f_out:

        word_count = 0
        line_count = 0

        for line in tqdm(f_in, desc="进度"):
            line = line.strip()
            if not line:  # 跳过空行
                continue

            # 使用jieba分词
            words = jieba.lcut(line, HMM=True)

            # 过滤停用词和其他不需要的词
            filtered_words = []
            for word in words:
                word = word.strip()
                if not word:  # 跳过空词
                    continue
                if word in stopwords:  # 跳过停用词
                    continue
                #if len(word) < 2:
                #    continue

                filtered_words.append(word)
                word_count += 1

            if filtered_words:
                f_out.write(' '.join(filtered_words) + '\n')
                line_count += 1

        # 输出统计
        print(f"\n处理完成!")
        print(f"处理行数: {line_count}")
        print(f"总词数: {word_count}")
        print(f"平均每行词数: {word_count / line_count:.1f}")


tokenize_with_stopwords(
    input_file="cleaned_chinese.txt",
    output_file="tokenized_with_stopwords.txt",
    stopwords_file="哈工大停用词表.txt"
)