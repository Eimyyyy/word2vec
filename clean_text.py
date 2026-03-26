#文本数据处理
import re
from opencc import OpenCC


def clean_chinese_text(input_file, output_file):
    cc = OpenCC('t2s')  # 繁体转简体

    with open(input_file, 'r', encoding='utf-8') as f_in, \
            open(output_file, 'w', encoding='utf-8') as f_out:

        total_lines = 0
        kept_lines = 0
        total_chars = 0

        for line in f_in:
            total_lines += 1

            #跳过空行
            if not line.strip():
                continue

            #繁体转简体
            simplified_line = cc.convert(line.strip())

            #只保留中文
            #[\u4e00-\u9fff] 基本汉字
            #[\u3400-\u4dbf] CJK扩展A区
            #[\u3000-\u303f] 中文标点符号
            chinese_chars = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f]', simplified_line)

            if chinese_chars:
                chinese_text = ''.join(chinese_chars)
                f_out.write(chinese_text + '\n')
                kept_lines += 1
                total_chars += len(chinese_text)

            # 显示进度
            if total_lines % 10000 == 0:
                print(f"已处理 {total_lines} 行，保留 {kept_lines} 行，{total_chars} 字符")

    print(f"原始文件行数: {total_lines}")
    print(f"保留的行数: {kept_lines}")
    print(f"总字符数: {total_chars}")
    print(f"输出文件: {output_file}")


clean_chinese_text("wiki_plain_text.txt", "cleaned_chinese.txt")